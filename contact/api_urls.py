from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.ContactAPIView.as_view(), name='api_contact'),
]
