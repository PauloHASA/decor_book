from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class NewUser():
    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length = 150, unique=True)
    full_name = models.CharField(max_length = 150)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_('about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)