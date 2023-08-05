import requests

from django.core.exceptions import ObjectDoesNotExist
from dj_active_campaign.active_campaign.connector import ActiveCampaignConnector


class CustomFieldAPI(ActiveCampaignConnector):
    RELATIVE_URL = 'fields'

    def query(self, limit=100):
        self.get(self.RELATIVE_URL, {'limit': limit})

    def get(self, id):
        self.get(self.RELATIVE_URL + f'/{id}')

    def create(self, data):
        if 'type' not in data and 'title' not in data:
            raise KeyError("type and title needed to create field")

        self.post(self.RELATIVE_URL, {'field': data})

    def update(self, id, data):
        self.put(self.RELATIVE_URL + f'/{id}', data={'field': data})

    def remove(self, id):
        self.delete(self.RELATIVE_URL + f'/{id}')