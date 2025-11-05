from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import TalentRegistrationForm, RecruiterRegistrationForm

# Talent Registration
def TalentRegForm(request):
    if request.method == 'POST':
        form = TalentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Talent account created successfully! Please login.")
            return redirect('login')
    else:
        form = TalentRegistrationForm()
    return render(request, 'register_talent.html', {'form': form})

# Recruiter Registration
def RecruiterRegForm(request):
    if request.method == 'POST':
        form = RecruiterRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Recruiter account created successfully! Please login.")
            return redirect('login')
    else:
        form = RecruiterRegistrationForm()
    return render(request, 'register_recruiter.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')  # you can accept username or email later
        password = request.POST.get('password')

        # Attempt authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)

        # If using email as login, try to fetch user by email and authenticate (optional)
        if user is None:
            # try email-based auth (only if you want email logins)
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
            else:
                return redirect('home')  # fallback
        else:
            messages.error(request, "Invalid username/email or password.")
    return render(request, 'login.html')

# Dashboards (simple placeholders)
def talent_dashboard(request):
    return render(request, 'talent_dashboard.html')

def recruiter_dashboard(request):
    return render(request, 'recruiter_dashboard.html')
