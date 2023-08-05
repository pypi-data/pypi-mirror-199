from django.core.exceptions import ObjectDoesNotExist
from integrations.models import Credential
from dj_active_campaign.forms import ActiveCampaignIntegrationForm


class ActiveCampaignIntegration(object):
    NAME = "Active Campaign Integration"

    site = None
    form_class = ActiveCampaignIntegrationForm

    def __init__(self, site):
        self.site = site
        self.instance = self.get_instance()

    def get_instance(self):
        try:
            return Credential.objects.get(name=self.NAME, site=self.site)
        except ObjectDoesNotExist:
            return None
    
    def save(self, data):
        if not self.instance:
            form = self.form_class(data)
        else:
            form = self.form_class(data, instance=self.instance)
        
        active_campaign = form.save(commit=False)
        active_campaign.name = self.NAME
        active_campaign.site = self.site
        active_campaign.save()