from rest_framework import serializers
from .models import JobContent

class JobContentSerializer(serializers.ModelSerializer):
    recruiter_name = serializers.CharField(source='recruiter.user.username',read_only = True)
    job_company_website = serializers.ReadOnlyField()
    job_company = serializers.ReadOnlyField()

    class Meta:
        model = JobContent
        fields = '__all__'
        read_only_fields = ['recruiter', 'company_name', 'company_website']