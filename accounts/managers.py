from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
     def create_user(self, email, first_name, last_name, password=None, **extra_fields):
         if not email:
             raise ValueError('Your email is mandatory, it will be your user name')
         if not first_name:
             raise ValueError('Your first name must be provided')
         if not last_name:
             raise ValueError('Your last name must be provided')
         
         email = self.normalize_email(email)
         user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
         user.set_password(password)
         user.save(using=self._db)
         return user

     def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
         extra_fields.setdefault('is_staff', True)
         extra_fields.setdefault('is_superuser', True)
         extra_fields.setdefault('is_active', True)

         return self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, **extra_fields)
     
     