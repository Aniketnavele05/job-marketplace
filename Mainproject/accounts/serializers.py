from rest_framework import serializers
from .models import JobContent, JobRole, Skill, Location

class JobRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRole
        fields = ['id', 'name']

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name']

class JobContentSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.user.username', read_only=True)
    job_company_website = serializers.ReadOnlyField()
    job_company = serializers.ReadOnlyField()

    # ✅ use nested serializers here
    job_role = JobRoleSerializer(many=True, read_only=True)
    needed_skills = SkillsSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = JobContent
        fields = '__all__'
        read_only_fields = ['recruiter', 'job_company', 'job_company_website']
