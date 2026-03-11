from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.ProjectListAPIView.as_view(), name='api_projects'),
    path('<int:pk>/', api_views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
]
