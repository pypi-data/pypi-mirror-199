import logging
import requests

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from dj_active_campaign.integrations import ActiveCampaignIntegration

logger = logging.getLogger(__name__)


class ActiveCampaignConnector(object):

    def __init__(self, site):
        self.response = None
        self.errors = None
        active_campaign_credentials = ActiveCampaignIntegration(site)

        if active_campaign_credentials.instance:
            self.url = active_campaign_credentials.instance.client_url + active_campaign_credentials.instance.client_id
            self.headers = {
                'Api-Token': active_campaign_credentials.instance.private_key,
                'Content-Type': 'application/json'
            }
        elif settings.ACTIVE_CAMPAIGN_URL and settings.ACTIVE_CAMPAIGN_KEY and settings.ACTIVE_CAMPAIGN_VERSION:
            self.url = settings.ACTIVE_CAMPAIGN_URL + settings.ACTIVE_CAMPAIGN_VERSION
            self.headers = {
                'Api-Token': settings.ACTIVE_CAMPAIGN_KEY,
                'Content-Type': 'application/json'
            }
        else:
            raise ObjectDoesNotExist("Active Campaign Credentials are not set")

    def post(self, relative_url, data):
        full_url = self.url + relative_url

        self.response = requests.post(full_url, headers=self.headers, json=data, timeout=1)
    
    def get(self, relative_url, params=None):
        full_url = self.url + relative_url

        self.response = requests.get(full_url, headers=self.headers, params=params)

    def put(self, relative_url, data, params=None):
        full_url = self.url + relative_url

        self.response = requests.put(full_url, headers=self.headers, params=params, json=data)

    def delete(self, relative_url):
        full_url = self.url + relative_url

        self.response = requests.delete(full_url, headers=self.headers)

    def is_response_valid(self):
        try:
            self.response.raise_for_status()
            
            return True

        except (requests.HTTPError, NameError) as exception:
            logger.exception(f"{exception}")
            logger.exception(f"{self.response.json()}")
            if 'errors' in self.response.json():
                self.errors = self.response.json().get('errors')
        
        return False
        

    def are_credentials_valid(self):
        response = requests.get(self.url + 'campaigns', headers=self.headers)
        
        if response.status_code == 200:
            return True
        
        return False
