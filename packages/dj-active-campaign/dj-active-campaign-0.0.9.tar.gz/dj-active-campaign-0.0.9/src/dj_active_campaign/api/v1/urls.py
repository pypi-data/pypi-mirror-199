from django.urls import path

from dj_active_campaign.api.v1 import views

app_name = "dj_active_campaign_api"

urlpatterns = [
    path('custom/field/<str:uuid>/create/', views.ActiveCampaignCustomFieldCreate.as_view(), name='ac-custom-field-create'),
    path('contacts/', views.ActiveCampaignContacts.as_view(), name='ac-contacts'),
    path('contact/create/', views.ActiveCampaignContactCreate.as_view(), name='ac-contact-create'),
    path('contact/update/', views.ActiveCampaignContactUpdate.as_view(), name='ac-contact-update'),
]