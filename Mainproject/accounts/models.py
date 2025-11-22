from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import JSONField
from phonenumber_field.modelfields import PhoneNumberField
# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('talent', 'Talent'),
        ('recruiter', 'Recruiter'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='talent')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


# -------------------------
# Shared models (used by both Talent and Recruiter)
# -------------------------
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)  # e.g. Backend, Frontend, Soft skill

    def __str__(self):
        return self.name


class JobRole(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class JobType(models.Model):
    """Used both for talent preferences (many) and job postings (single type per job)."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# -------------------------
# Talent Models
# -------------------------
class TalentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='talent_profile')
    profile_picture = models.ImageField(upload_to='talent_profile_pic/',
        null=True, 
        blank=True, 
        validators=[FileExtensionValidator(['jpeg','jpg','webp'])]
    )
    about = models.TextField(default="")
    gender = models.CharField(max_length=20, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    social = models.JSONField(default=dict,blank=True,null=True)
    open_to_work = models.BooleanField(default=False)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='talents')
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.username


class JobPreference(models.Model):
    profile = models.OneToOneField(TalentProfile, on_delete=models.CASCADE, related_name='preferences')
    desired_titles = models.ManyToManyField(JobRole, blank=True, related_name='preferred_by_talents')
    job_types = models.ManyToManyField(JobType, blank=True, related_name='preferred_by_talents')
    preferred_locations = models.ManyToManyField(Location, blank=True, related_name='preferred_by_talents')

    @property
    def talent_skills(self):
        return self.profile.skills

    def __str__(self):
        return f"Preferences of {self.profile.user.username}"


class Experience(models.Model):
    profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    months = models.FloatField(help_text='Duration in months', null=True, blank=True)

    def __str__(self):
        return f"{self.profile.user.username} at {self.company_name}"


# -------------------------
# Recruiter Models
# -------------------------
class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=150)
    company_description = models.TextField(blank=True)
    company_website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.company_name})"


# -------------------------
# Job Content (Jobs posted by Recruiters)
# -------------------------
class JobContent(models.Model):
    EXPERIENCE_LEVEL_CHOICES = [
        ('Internship', 'Internship'),
        ('Entry Level', 'Entry Level'),
        ('Mid Level', 'Mid Level'),
        ('Senior Level', 'Senior Level'),
    ]

    recruiter = models.ForeignKey(
        RecruiterProfile, on_delete=models.CASCADE, related_name='jobs'
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    job_title = models.CharField(max_length=100)

    job_role = models.ManyToManyField(
        JobRole, related_name='jobs'
    )
    needed_skills = models.ManyToManyField(
        Skill, related_name='jobs'
    )
    job_type = models.ForeignKey(
        JobType, on_delete=models.SET_NULL, null=True, related_name='jobs'
    )  # single type per job
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='jobs'
    )

    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, default='INR')
    benefits = models.CharField(max_length=500, blank=True)
    job_description = models.TextField()
    is_active = models.BooleanField(default=True)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES, blank=True)
    apply_email = models.EmailField(blank=True, null=True)

    @property
    def job_company(self):
        return self.recruiter.company_name

    @property
    def job_company_website(self):
        return self.recruiter.company_website

    def __str__(self):
        return f"{self.job_title} at {self.recruiter.company_name}"