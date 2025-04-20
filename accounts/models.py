from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from .managers import CustomUserManager
import uuid
from django.core.mail import send_mail
import os



#Function to generate random file name for uploaded image files
def ramdom_file_name(instance, filename):
    file_extension = filename.split('.')[-1]
    random_filename = f'{uuid.uuid4()}.{file_extension}'
    return os.path.join('avatars', random_filename) 

#Main custom user model
class Users(AbstractBaseUser, PermissionsMixin):
    
     ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('standard_user', 'Standard User'),
        ('power_user', 'Power User'),
        ('guest', 'Guest'),
     ]

     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
     email = models.EmailField(unique=True)
     first_name = models.CharField(max_length=30, blank=True)
     last_name = models.CharField(max_length=30, blank=True)
     user_name = models.CharField(max_length=30, unique=True)
     avatar = models.ImageField(upload_to=ramdom_file_name, blank=True, null=True, default='default_user_img.png')
     is_active = models.BooleanField(default=False)
     is_staff = models.BooleanField(default=False)
     is_superuser = models.BooleanField(default=False)
     date_joined = models.DateTimeField(auto_now_add=True)
     last_login = models.DateTimeField(auto_now=True)
     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='standard_user')

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = ['first_name', 'last_name', 'user_name']
     
     objects = CustomUserManager()
     
     class Meta:
         verbose_name = 'Users'
         verbose_name_plural = 'Users'

     def __str__(self):
         return self.email

     def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
        