from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    JobContentView,
    JobtypeView,
    JobChoices,
    SkillsView,
    LocationView,
    JobRoleView,
    IndexView,
    registrationView,
    UserInfoView
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
    path("api/login/", TokenObtainPairView.as_view(), name="jwt_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    # --- Web Routes ---
    path('',IndexView.as_view(),name='home'),
    path('api/register/', registrationView.as_view(), name='api_register'),
    path('api/user-info/', views.UserInfoView.as_view(), name='user_info'),
    path('dashboard/talent/', views.talent_dashboard, name='talent_dashboard'),
    path('dashboard/recruiter/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('job/<int:id>/', views.job_detail_page, name='job_detail'),
]
