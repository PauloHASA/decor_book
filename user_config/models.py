from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

PROFISSION_CHOICES = [
    ('arquiteto', 'Arquiteto'),
    ('carpinteiro', 'Carpinteiro'),
    ('designer', 'Designer'),
    ('engenheiro', 'Engenheiro'),
    ('eletricista', 'Eletricista'),
    ('gesseiro', 'Gesseiro'),
    ('pedreiro', 'Pedreiro'),
    ('pintor', 'Pintor'),
]
class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, user_name, full_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_client', True)
        other_fields.setdefault('is_professional', True)
        other_fields.setdefault('is_company', True)
        other_fields.setdefault('is_construction', True)
        
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        return self.create_user(email, user_name, full_name, password, **other_fields)
    
    def create_user(self, email, user_name, full_name, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          full_name=full_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    objects = CustomAccountManager()
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_client = models.BooleanField(default=True)
    is_professional = models.BooleanField(default=True)
    is_company = models.BooleanField(default=True)
    is_construction = models.BooleanField(default=True)
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length = 150, unique=True)
    full_name = models.CharField(max_length = 150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'full_name']
    
    def __str__(self):
        return self.user_name
    

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    is_client = models.BooleanField(default=True)
    profession = models.CharField(max_length=100, choices=PROFISSION_CHOICES)


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    is_professional = models.BooleanField(default=True)
    profession = models.CharField(max_length=100, choices=PROFISSION_CHOICES)
    site = models.CharField(max_length=100)

    

class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    fantasy_name = models.CharField(max_length=100)
    is_company = models.BooleanField(default=True)
    product = models.CharField(max_length=100)
    site = models.CharField(max_length=100)

    

class ConstructionProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    is_construction = models.BooleanField(default=True)
    site = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100)
