from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
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
)
from .serializers import (
    JobContentSerializer,
    JobUpdateSerializer,
    SkillsSerializer,
    JobRoleSerializer,
    LocationSerializer,
)
from .permissions import IsRecruiterOwner


# ------------------------------------------
# 🔹 AUTHENTICATION VIEWS
# ------------------------------------------
def TalentRegForm(request):
    """Handle Talent Registration"""
    if request.method == 'POST':
        form = TalentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Talent account created successfully! Please login.")
            return redirect('login')
    else:
        form = TalentRegistrationForm()
    return render(request, 'register_talent.html', {'form': form})


def RecruiterRegForm(request):
    """Handle Recruiter Registration"""
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recruiter account created successfully! Please login.")
            return redirect('login')
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'register_recruiter.html', {'form': form})


def login_view(request):
    """User Login (supports username or email login)"""
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try login by username
        user = authenticate(request, username=username_or_email, password=password)

        # Try login by email if username fails
        if user is None:
            from .models import CustomUser
            try:
                u = CustomUser.objects.get(email=username_or_email)
                user = authenticate(request, username=u.username, password=password)
            except CustomUser.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            if user.user_type == 'talent':
                return redirect('talent_dashboard')
            elif user.user_type == 'recruiter':
                return redirect('recruiter_dashboard')
            return redirect('home')
        else:
            messages.error(request, "Invalid username/email or password.")
    return render(request, 'login.html')


# ------------------------------------------
# 🔹 DASHBOARD VIEWS
# ------------------------------------------
@login_required(login_url='/login/')
def talent_dashboard(request):
    return render(request, 'talent_dashboard.html')


@login_required(login_url='/login/')
def recruiter_dashboard(request):
    return render(request, 'recruiter_dashboard.html')


# ------------------------------------------
# 🔹 JOB CONTENT API (CRUD)
# ------------------------------------------
class JobContentView(viewsets.ModelViewSet):
    """Manage Job Posts (Create/Update/Delete/View)"""
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
        recruiter = self.request.user.recruiter_profile
        serializer.save(recruiter=recruiter)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsRecruiterOwner]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]


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
class SkillsView(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillsSerializer


class LocationView(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class JobRoleView(viewsets.ReadOnlyModelViewSet):
    queryset = JobRole.objects.all()
    serializer_class = JobRoleSerializer


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
