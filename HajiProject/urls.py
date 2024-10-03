"""
URL configuration for HajiProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from  StudentApp import views

urlpatterns = [
    path('', views.student_login, name='login'),
    path('register/', views.student_register, name='student_register'),
    path('login/', views.student_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feedback/', views.give_feedback, name='give_feedback'),
    path('feedback_success/<str:student_id>/<str:student_name>/', views.feedback_success, name='feedback_success'),
    path('feedback_result/',views.get_counselor_feedback,name='feedback_result'),
    path('', lambda request: redirect('login')),
    path('fill_details/', views.fill_details, name='fill_details'),  # Correct URL for fill_details
    path('fill-skills/', views.student_skill_form_view, name='student_skill_form'),
    path('experience/', views.fill_experience_details, name='student_experience_form'),
    path('student/recommendation/', views.student_recommendation_view, name='student_recommendation'),
    path('student-progress/', views.student_track_progress_view, name='student_track_progress'),
    path('recruiter/login/', views.recruiter_login, name='recruiter_login'),
    path('recruiter/dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('recruiter/register/', views.recruiter_register, name='recruiter_register'),
    path('recruiter/logout/', views.recruiter_logout, name='logout'),
]
