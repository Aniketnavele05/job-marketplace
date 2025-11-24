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
        password = validated_data.pop('password')# Remove password from normal field for seprate use
        user = CustomUser(**validated_data)# Create user without password
        user.set_password(password)#H ashesh password
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
    # ---------------- READ ONLY (Talent View) ---------------- #
    needed_skills = SkillsSerializer(many=True, read_only=True)
    job_role = JobRoleSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    job_type = JobTypeSerializer(read_only=True)
    recruiter = serializers.PrimaryKeyRelatedField(read_only=True)
    
    # ---------------- WRITE ONLY (Recruiter Input) ---------------- #
    needed_skills_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    job_role_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    location_name = serializers.CharField(write_only=True, required=False)
    job_type_name = serializers.CharField(write_only=True, required=False)

    # ---------------- Recruiter Info (Read Only) ---------------- #
    job_company = serializers.ReadOnlyField(source='recruiter.company_name')
    job_company_website = serializers.ReadOnlyField(source='recruiter.company_website')

    class Meta:
        model = JobContent
        fields = [
            'id', 'recruiter', 'job_title',

            # Read-only nested for talent
            'needed_skills', 'job_role', 'location', 'job_type',

            # Write-only for recruiter
            'needed_skills_names', 'job_role_names',
            'location_name', 'job_type_name',

            # Other fields
            'salary_min', 'salary_max', 'currency',
            'benefits', 'job_description', 'is_active', 'experience_level',
            'apply_email',

            # Recruiter info
            'job_company', 'job_company_website'
        ]

    # ---------------- CREATE ---------------- #
    def create(self, validated_data):

        skills_data = validated_data.pop('needed_skills_names', [])
        roles_data = validated_data.pop('job_role_names', [])
        location_data = validated_data.pop('location_name', None)
        job_type_data = validated_data.pop('job_type_name', None)

        # Create job
        job = JobContent.objects.create(**validated_data)
        # Skills (Many-to-many)
        skill_list = []
        for skill_name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=skill_name)
            skill_list.append(skill)
        job.needed_skills.set(skill_list)

        # Job roles (Many-to-many)
        job_role_list = []
        for role_name in roles_data:
            role, _ = JobRole.objects.get_or_create(name=role_name)
            job_role_list.append(role)
        job.job_role.set(job_role_list)

        # Location (FK)
        if location_data:
            location, _ = Location.objects.get_or_create(name=location_data)
            job.location = location
            job.save()

        # Job type (FK)
        if job_type_data:
            jt, _ = JobType.objects.get_or_create(name=job_type_data)
            job.job_type = jt
            job.save()

        return job

    def update(self, instance, validated_data):

        skills_data = validated_data.pop('needed_skills_names', None)
        roles_data = validated_data.pop('job_role_names', None)
        location_data = validated_data.pop('location_name', None)
        job_type_data = validated_data.pop('job_type_name', None)

    # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

    # Update skills (Many-to-Many)
        if skills_data is not None:
            skill_list = []
            for name in skills_data:
                skill, _ = Skill.objects.get_or_create(name=name)
                skill_list.append(skill)
            instance.needed_skills.set(skill_list)

    # Update job roles (Many-to-Many)
        if roles_data is not None:
            role_list = []
            for name in roles_data:
                role, _ = JobRole.objects.get_or_create(name=name)
                role_list.append(role)
            instance.job_role.set(role_list)

    # Update location (FK)
        if location_data is not None:
            location, _ = Location.objects.get_or_create(name=location_data)
            instance.location = location

    # Update job type (FK)
        if job_type_data is not None:
            jt, _ = JobType.objects.get_or_create(name=job_type_data)
            instance.job_type = jt

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