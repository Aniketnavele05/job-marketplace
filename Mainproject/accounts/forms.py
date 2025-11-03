from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import TalentProfile , RecruiterProfile , CustomUser

class BaseUserForm(UserCreationForm):
    username = forms.CharField(max_length=24, required=True)
    first_name = forms.CharField( max_length=12, required=True)
    last_name = forms.CharField( max_length=12, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit :
            user.save()
        return user
    
class TalentUserForm(UserCreationForm):
    dob = forms.DateField( required=False)
    locations = forms.CharField( max_length=50, required=False)

    class Meta:
        models = TalentProfile
        fields = TalentProfile.Meta.data = ['DOB','locations']