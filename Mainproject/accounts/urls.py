from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    JobContentView,
    JobtypeView,
    JobChoices,
    SkillsView,
    LocationView,
    JobRoleView
)

# Router for Job CRUD (Create/Read/Update/Delete)
router = DefaultRouter()
router.register(r'jobs', JobContentView, basename='job')

urlpatterns = [
    # --- API Endpoints ---
    path('api/', include(router.urls)),  # Job CRUD
    path('api/jobs-choices/', JobChoices.as_view(), name='job_choices'),
    path('api/jobtype/', JobtypeView.as_view(), name='jobtypes'),
    path('api/skills/', SkillsView.as_view(), name='skills'),
    path('api/jobroles/', JobRoleView.as_view(), name='jobroles'),
    path('api/locations/', LocationView.as_view(), name='locations'),

    # --- Web Routes ---
    path('registration/talent/', views.TalentRegForm, name='register_talent'),
    path('registration/recruiter/', views.RecruiterRegForm, name='register_recruiter'),
    path('login/', views.login_view, name='login'),
    path('dashboard/talent/', views.talent_dashboard, name='talent_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('job/<int:id>/', views.job_detail_page, name='job_detail'),
]
