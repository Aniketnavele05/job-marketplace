from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import JobContentView

router = DefaultRouter()
router.register(r'jobs', JobContentView, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('registration/talent/', views.TalentRegForm, name='register_talent'),
    path('registration/recruiter/', views.RecruiterRegForm, name='register_recruiter'),
    path('login/', views.login_view, name='login'),
    path('dashboard/talent/', views.talent_dashboard, name='talent_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
]
