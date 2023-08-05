import logging

from dj_active_campaign.models import CustomField
from dj_active_campaign.active_campaign import CustomFieldAPI, ContactAPI

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.views.generic import TemplateView, ListView, View


logger = logging.getLogger(__name__)


def get_site_from_request(request):
    if hasattr(request, 'site'):
        return request.site
    return get_current_site(request)


class IndexView(TemplateView):
    template_name = "dj_active_campaign/index.html"

class CustomFieldsListView(ListView):
    template_name = "dj_active_campaign/custom_fields.html"
    model = CustomField

    def get_queryset(self):
        return CustomField.on_site.all()

