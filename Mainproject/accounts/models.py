from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('talent','Talent'),
        ('recruiter','Recruiter')
    )

    user_type = models.CharField( max_length=20,choices=USER_TYPE_CHOICES,default='talent')

    def __str__(self):
        return f'{self.username} = {self.user_type}'
    
