from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import IntegrityError
from django.templatetags.static import static

from .controllers import FolderUserPost


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
        other_fields.setdefault('is_professional', False)
        other_fields.setdefault('is_company', False)
        other_fields.setdefault('is_construction', False)
        
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
        user = self.model(email=email, user_name=user_name, full_name=full_name, **other_fields)
        user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            # Handle the case when the email already exists
            raise ValueError(_('Email address already exists'))
        return user


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    objects = CustomAccountManager()
    is_staff = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_organic = models.BooleanField(default=False)
    is_marketing = models.BooleanField(default=False)
    
    is_client = models.BooleanField(default=False)
    is_professional = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    is_construction = models.BooleanField(default=False)

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length = 150, unique=True)
    full_name = models.CharField(max_length = 150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'full_name']
    
    @property
    def avatar(self):
        try:
            if self.is_client:
                avatar = self.client_profile.profile_picture.url
            elif self.is_professional:
                avatar = self.professional_profile.profile_picture.url
            elif self.is_company:
                avatar = self.company_profile.company_profile_pics.url
        except:
            avatar = static('global/media/img/default.jpg')
        return avatar
    
    def __str__(self):
        return self.user_name
    

class ClientProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name="client_profile")
    is_client = models.BooleanField(default=True)
    profession = models.CharField(max_length=100, choices=PROFISSION_CHOICES)


class ProfessionalProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name="professional_profile")
    is_professional = models.BooleanField(default=True)
    profession = models.CharField(max_length=100, choices=PROFISSION_CHOICES)
    site = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to="users_folder/profile_picture/", blank=True, null=True)


class CompanyProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name="company_profile")
    fantasy_name = models.CharField(max_length=100)
    is_company = models.BooleanField(default=True)
    product = models.CharField(max_length=100)
    site = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='users_folders/company_profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.fantasy_name

    

class ConstructionProfile(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    is_construction = models.BooleanField(default=True)
    site = models.CharField(max_length=100)
    fantasy_name = models.CharField(max_length=100)
