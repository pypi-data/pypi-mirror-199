from django.urls import path, re_path
from dj_active_campaign import views
from dj_active_campaign.api.v1 import urls as api_urls

urlpatterns = [
    path('', views.IndexView.as_view(), name='dj-active-campaign-index'),
    path('custom/fields/', views.CustomFieldsListView.as_view(), name='custom-fields'),
    # path('simple/', views.PackageView.as_view(), name='dj_active_campaign-simple'),
    # path('simple/<slug:slug>/', views.VersionView.as_view(), name='dj_active_campaign-simple-version'),
]

