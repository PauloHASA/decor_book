from django.db import models
from user_config.models import CustomUserModel
# Create your models here.

class Dataframe(models.Model):
    request_id = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE, null=True)
    admin_id = models.CharField(max_length=200, null=True)
    name = models.TextField(null=True)
    addr_pstl_cd = models.CharField(max_length=200, null=True)
    latitude = models.CharField(max_length=100, null=True)
    longitude = models.CharField(max_length=100, null=True)
    coord_geoc = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=150, null=True)