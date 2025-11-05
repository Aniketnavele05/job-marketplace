from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# -------------------------
# Custom User
# -------------------------
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('talent','Talent'),
        ('recruiter','Recruiter')
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='talent')

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------
# Talent models
# -------------------------
class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, blank=True, null=True)  # e.g., Backend, Frontend, Soft skill

    def __str__(self):
        return self.name

class JobTitle(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


class TalentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='talent_profile')
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=50, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    resume = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(['pdf','doc','docx'])],
        null=True, blank=True
    )

    def __str__(self):
        return self.user.username


class JobPreference(models.Model):
    JobType = (
        ('Full_time','FULL_TIME'),
        ('Part_time','PART_TIME'),
        ('Remote','Remote'),
        ('Open to all','OPEN_TO_ALL')
    )
    profile = models.OneToOneField(TalentProfile, on_delete=models.CASCADE, related_name='preferences')
    desired_titles = models.ManyToManyField(JobTitle, blank=True, related_name='preferred_by_talents')
    job_types = models.CharField(max_length=20, choices=JobType, null=False, blank=False, default='Open to all')
    preferred_locations = models.ManyToManyField(Location, blank=True, related_name='preferred_by_talents')

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
        return f'{self.profile.user.username} at {self.company_name}'


# -------------------------
# Recruiter models
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
