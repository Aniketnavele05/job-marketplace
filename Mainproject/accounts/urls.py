from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import JobContentView , JobChoices , SkillsView , LocationView , JobRoleView

router = DefaultRouter()
router.register(r'jobs', JobContentView, basename='job')
router.register(r'skills',SkillsView,basename='skill')
router.register(r'jobroles',JobRoleView,basename='jobrole')
router.register(r'locations', LocationView, basename='location')

urlpatterns = [
    path('api/jobs-choices/',JobChoices.as_view(),name='job_choices'),
    path('api/', include(router.urls)),
    path('registration/talent/', views.TalentRegForm, name='register_talent'),
    path('registration/recruiter/', views.RecruiterRegForm, name='register_recruiter'),
    path('login/', views.login_view, name='login'),
    path('dashboard/talent/', views.talent_dashboard, name='talent_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
]
