from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework import viewsets, generics, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from .forms import TalentRegistrationForm, RecruiterRegistrationForm
from .models import (
    JobContent,
    TalentProfile,
    RecruiterProfile,
    Skill,
    Location,
    JobRole,
    JobType,
)
from .serializers import (
    JobContentSerializer,
    JobUpdateSerializer,
    SkillsSerializer,
    JobRoleSerializer,
    LocationSerializer,
    JobTypeSerializer,
    RegSerializer
)
from .permissions import IsRecruiterOwner


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
# ------------------------------------------
# 🔹 AUTHENTICATION VIEWS
# ------------------------------------------
class registrationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        serialzer  = RegSerializer(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return Response({'message':"user create"})
        else:
            return Response(serialzer.errors)


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]  # Only accessible with JWT
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        return Response({
            "username": request.user.username,
            "user_type": request.user.user_type
        })
    
# ------------------------------------------
# 🔹 DASHBOARD VIEWS
# ------------------------------------------
@login_required(login_url='/')
def talent_dashboard(request):
    return render(request, 'talent_dashboard.html')

@login_required(login_url='/login/')
def recruiter_dashboard(request):
    return render(request, 'recruiter_dashboard.html')


# ------------------------------------------
# 🔹 JOB CONTENT API (CRUD)
# ------------------------------------------
class JobContentView(viewsets.ModelViewSet):
    serializer_class = JobContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'recruiter_profile'):
            return JobContent.objects.filter(recruiter=user.recruiter_profile)
        elif hasattr(user, 'talent_profile'):
            return JobContent.objects.filter(is_active=True)
        return JobContent.objects.none()

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return JobUpdateSerializer
        return JobContentSerializer

    def perform_create(self, serializer):
        """Create job with recruiter and set foreign keys/many-to-many fields"""
        recruiter = self.request.user.recruiter_profile
        job = serializer.save(recruiter=recruiter)

        # Handle Many-to-Many fields
        needed_skills_ids = self.request.data.get("needed_skills", [])
        if needed_skills_ids:
            skills = Skill.objects.filter(id__in=needed_skills_ids)
            job.needed_skills.set(skills)

        job_role_ids = self.request.data.get("job_role", [])
        if job_role_ids:
            roles = JobRole.objects.filter(id__in=job_role_ids)
            job.job_role.set(roles)

        # Handle ForeignKey fields
        location_id = self.request.data.get("location")
        if location_id:
            try:
                job.location = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                pass

        job_type_id = self.request.data.get("job_type")
        if job_type_id:
            try:
                job.job_type = JobType.objects.get(id=job_type_id)
            except JobType.DoesNotExist:
                pass

        job.save()


# ------------------------------------------
# 🔹 STATIC CHOICES (for dropdowns)
# ------------------------------------------
class JobChoices(APIView):
    """Expose job-related choice fields"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "job_type_choices": JobContent.JobType,
            "experience_level_choices": JobContent.ExperienceLevelChoices,
        })


# ------------------------------------------
# 🔹 STATIC DATASETS (Skills, Locations, Roles)
# ------------------------------------------
class SkillsView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class LocationView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class JobRoleView(generics.ListAPIView):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class JobtypeView(generics.ListAPIView):
    queryset = JobType.objects.all()
    serializer_class = JobTypeSerializer

# ------------------------------------------
# 🔹 JOB DETAIL PAGE (Frontend Render)
# ------------------------------------------
@login_required(login_url='/login/')
def job_detail_page(request, id):
    """Render single job detail page"""
    user_type = request.user.user_type
    context = {
        'job_id': id,
        'user_type': user_type,
    }
    return render(request, 'job_detail.html', context)
