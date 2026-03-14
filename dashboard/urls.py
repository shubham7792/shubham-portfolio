from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),

    # Profile
    path('profile/', views.profile_edit, name='dashboard_profile'),

    # Skills
    path('skills/', views.skill_list, name='dashboard_skills'),
    path('skills/add/', views.skill_add, name='dashboard_skill_add'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='dashboard_skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='dashboard_skill_delete'),

    # Projects
    path('projects/', views.project_list, name='dashboard_projects'),
    path('projects/add/', views.project_add, name='dashboard_project_add'),
    path('projects/<int:pk>/edit/', views.project_edit, name='dashboard_project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='dashboard_project_delete'),

    # Technologies
    path('technologies/', views.tech_list, name='dashboard_technologies'),
    path('technologies/add/', views.tech_add, name='dashboard_tech_add'),
    path('technologies/<int:pk>/edit/', views.tech_edit, name='dashboard_tech_edit'),
    path('technologies/<int:pk>/delete/', views.tech_delete, name='dashboard_tech_delete'),

    # Education
    path('education/', views.education_list, name='dashboard_education'),
    path('education/add/', views.education_add, name='dashboard_education_add'),
    path('education/<int:pk>/edit/', views.education_edit, name='dashboard_education_edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='dashboard_education_delete'),

    # Experience
    path('experience/', views.experience_list, name='dashboard_experience'),
    path('experience/add/', views.experience_add, name='dashboard_experience_add'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='dashboard_experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='dashboard_experience_delete'),

    # Messages
    path('messages/', views.message_list, name='dashboard_messages'),
    path('messages/<int:pk>/', views.message_detail, name='dashboard_message_detail'),
    path('messages/<int:pk>/status/', views.message_status, name='dashboard_message_status'),
    path('messages/<int:pk>/delete/', views.message_delete, name='dashboard_message_delete'),
     path('messages/<int:pk>/reply/', views.message_reply, name='dashboard_message_reply'),

    # Users
    path('users/', views.user_list, name='dashboard_users'),
    path('users/<int:pk>/toggle-staff/', views.user_toggle_staff, name='dashboard_user_toggle'),
]