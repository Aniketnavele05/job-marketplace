from rest_framework import serializers
from .models import JobContent, JobRole, Skill, Location , JobType

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

class JobTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobType
        fields = ['id','name']

class JobContentSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.user.username', read_only=True)
    job_company_website = serializers.ReadOnlyField()
    job_company = serializers.ReadOnlyField()

    # ✅ use nested serializers here
    job_role = JobRoleSerializer(many=True, read_only=True)
    needed_skills = SkillsSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    job_type = JobTypeSerializer(read_only = True)
    class Meta:
        model = JobContent
        fields = '__all__'
        read_only_fields = ['recruiter', 'job_company', 'job_company_website']

class JobUpdateSerializer(serializers.ModelSerializer):
    job_role = serializers.PrimaryKeyRelatedField(queryset = JobRole.objects.all(),many=True)
    needed_skills = serializers.PrimaryKeyRelatedField(queryset = Skill.objects.all(),many = True)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    job_type = serializers.PrimaryKeyRelatedField(queryset=JobType.objects.all())
    class Meta:
        model = JobContent
        fields = [
            'job_title','job_role','needed_skills','job_type','location',
            'salary_min','salary_max','currency','benefits',
            'job_description','experience_level','apply_email','is_active'
        ]