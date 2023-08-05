from dj_active_campaign.models import CustomField
from django import forms
from django.utils.translation import gettext_lazy as _
from integrations.models import Credential


class ActiveCampaignIntegrationForm(forms.ModelForm):

    class Meta:
        model = Credential
        fields = ['client_url', 'private_key', 'client_id']
        labels = {
            'client_url': _("Active Campaign URL"),
            'private_key': _("Active Campaign Key"),
            'client_id': _("API Version")
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_url'].required = True
        self.fields['private_key'].required = True
        self.fields['client_id'].required = True


class CustomFieldForm(forms.ModelForm):

    class Meta:
        model = CustomField
        fields = []
