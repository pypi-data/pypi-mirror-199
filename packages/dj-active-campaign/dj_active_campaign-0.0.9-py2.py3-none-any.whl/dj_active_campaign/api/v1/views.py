import json
import logging

from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.urls import reverse_lazy

from dj_active_campaign.models import CustomField, CustomFieldTypes
from dj_active_campaign.active_campaign import ContactAPI, CustomFieldAPI
from dj_active_campaign.views import get_site_from_request


logger = logging.getLogger(__name__)


class ActiveCampaignCustomFieldCreate(View):
    default_redirect = reverse_lazy('custom-fileds')

    def post(self, request, *args, **kwargs):
        custom_field = CustomField.on_site.get(uuid=kwargs.get('uuid'))

        custom_field_api = CustomFieldAPI(get_site_from_request(request))
        custom_field_api.create({'type': custom_field.ac_type, 'title': custom_field.ac_title})

        if not custom_field_api.is_response_valid():
            logger.error(custom_field_api.errors)

            return redirect(request.META.get('HTTP_REFERER', self.default_redirect))

        custom_field.ac_id = custom_field_api.response.json()['field']['id']
        custom_field.save()
        
        return redirect(request.META.get('HTTP_REFERER', self.default_redirect))


class ActiveCampaignContactCreate(View):
    default_redirect = reverse_lazy('dj-active-campaign-index')

    def post(self, request, *args, **kwargs):
        site = get_site_from_request(request)
        contact_api = ContactAPI(site)

        contact_api.create(json.loads(request.body))

        if not contact_api.is_response_valid():
            logger.error(contact_api.errors)

        return redirect(request.META.get('HTTP_REFERER', self.default_redirect))


class ActiveCampaignContactUpdate(View):
    default_redirect = reverse_lazy('dj-active-campaign-index')

    def post(self, request, *args, **kwargs):
        contact_api = ContactAPI(get_site_from_request(request))

        contact_api.update(json.loads(request.body))

        if not contact_api.is_response_valid():
            logger.error(contact_api.errors)
        
        return redirect(request.META.get('HTTP_REFERER', self.default_redirect))


class ActiveCampaignContacts(View):

    def get(self, request, *args, **kwargs):

        contact_api = ContactAPI(get_site_from_request(request))

        contact_api.query()

        if not contact_api.is_response_valid():
            logger.error(contact_api.errors)

            return JsonResponse(contact_api.errors)

        return JsonResponse(contact_api.response.json().get('contacts'), safe=False)
