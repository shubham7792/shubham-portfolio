from django.urls import path
from . import api_views

urlpatterns = [
    path('profile/', api_views.ProfileAPIView.as_view(), name='api_profile'),
    path('skills/', api_views.SkillListAPIView.as_view(), name='api_skills'),
]
