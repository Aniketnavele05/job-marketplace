from rest_framework import serializers
from .models import CustomUser, JobContent, JobRole, Skill, Location , JobType , TalentProfile, RecruiterProfile

class RegSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','password','email','user_type']

        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')#Remove password from normal field for seprate use
        user = CustomUser(**validated_data)#Create user without password
        user.set_password(password)#Hashesh pass
        user.save()
        if user.user_type == 'talent':
            TalentProfile.objects.create(user=user)
        elif user.user_type == 'recruiter':
            RecruiterProfile.objects.create(user=user)
        return user
        

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
    needed_skills = SkillsSerializer(many=True, read_only=True)
    job_role = JobRoleSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    job_type = JobTypeSerializer(read_only=True)

    class Meta:
        model = JobContent
        fields = [
            'id', 'job_title', 'job_description', 'needed_skills', 
            'job_role', 'location', 'job_type', 'experience_level', 
            'salary_min', 'salary_max', 'apply_email', 'is_active',
            'recruiter', 'job_company', 'job_company_website'
        ]

class JobUpdateSerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    job_type = serializers.PrimaryKeyRelatedField(queryset=JobType.objects.all())
    job_role = serializers.PrimaryKeyRelatedField(queryset=JobRole.objects.all(), many=True)
    needed_skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)

    class Meta:
        model = JobContent
        fields = [
            'job_title','job_role','needed_skills','job_type','location',
            'salary_min','salary_max','currency','benefits',
            'job_description','experience_level','apply_email','is_active'
        ]
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('needed_skills', None)
        job_role_data = validated_data.pop('job_role', None)

        if job_role_data is not None:
            instance.job_role.set(job_role_data)
        if skills_data is not None:
            instance.needed_skills.set(skills_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class TalentProfileSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()
    skills = SkillsSerializer(many=True,read_only=True)
    class Meta:
        model = TalentProfile
        fields =  ['id', 'profile_picture', 'about', 'phone_number', 'open_to_work',
                'dob', 'location', 'skills', 'resume', 'social']
        
    def get_user_info(self,obj:TalentProfile)->dict:
        user = obj.user
        return{
            "username":user.username,
            "email":user.email
        }

class TalentProfileUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True)
    
    class Meta:
        model = TalentProfile
        fields = ['about', 'phone_number', 'open_to_work', 'dob', 'location', 'social', 'skills']
    
    def update(self, instance, validated_data):
        skills_data = validated_data.pop('skills', None)
        if skills_data is not None:
            instance.skills.set(skills_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class TalentProfileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentProfile
        fields = ['resume','profile_picture']