from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, TalentProfile, RecruiterProfile, Skill, JobTitle, Location, Experience, JobPreference ,JobContent

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')

admin.site.register(TalentProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Skill)
admin.site.register(JobTitle)
admin.site.register(Location)
admin.site.register(Experience)
admin.site.register(JobPreference)
admin.site.register(JobContent)