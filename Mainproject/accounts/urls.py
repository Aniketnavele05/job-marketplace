from django.urls import path
from . import views

urlpatterns = [
    path('registration/talent/', views.TalentRegForm, name='register_talent'),
    path('registration/recruiter/', views.RecruiterRegForm, name='register_recruiter'),
    path('login/', views.login_view, name='login'),
    path('dashboard/talent/', views.talent_dashboard, name='talent_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
]
