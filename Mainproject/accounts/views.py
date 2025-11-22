from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from rest_framework import viewsets, generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
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
    SkillsSerializer,
    JobRoleSerializer,
    LocationSerializer,
    JobTypeSerializer,
    RegSerializer
)
from .permissions import IsRecruiter


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
    queryset = JobContent.objects.all()
    serializer_class = JobContentSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_permissions(self):
        if self.action in ['list','retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(),IsRecruiter()]

    def perform_create(self,serializer):
        serializer.save(recruiter=self.request.user.recruiter_profile)
        

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
