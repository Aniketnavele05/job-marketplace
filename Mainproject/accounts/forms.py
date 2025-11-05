from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class TalentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.user_type = 'talent'
        if commit:
            user.save()
        return user


class RecruiterRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.user_type = 'recruiter'
        if commit:
            user.save()
        return user
