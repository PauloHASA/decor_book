from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import get_valid_filename
from django.utils.text import get_valid_filename
from user_config.models import CustomUserModel
from user_config.controllers import FolderUserPost
from user_config.storages import UserImageStorage
from user_config.storages import UserImageStorage
# Create your models here.


class NewProject(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    partner = models.CharField(max_length=150, blank=True, null=True)
    summary = models.TextField()
    data_initial = models.DateField(blank=True, null=True)
    data_final= models.DateField(blank=True, null=True)
    area = models.CharField(max_length=150)
    rooms = models.CharField(max_length=150)
    style = models.CharField(max_length=150, blank=True, null=True)
    categories = models.CharField(max_length=150, blank=True, null=True)
    add_stores = models.CharField(max_length=150, blank=True, null=True)
    
    def clean(self):
        if self.data_final is not None and self.data_initial is not None:
            if self.data_final < self.data_initial:
                raise ValidationError("A data final não pode ser anterior á data inicial.")

class ImagePortfolio(models.Model):
    new_project = models.ForeignKey(NewProject, on_delete=models.CASCADE)
    img_upload = models.ImageField(upload_to=FolderUserPost.image_filename)
    
    def save(self, *args, **kwargs):
        file_name = self.img_upload.name
        valid_filename = get_valid_filename(file_name)
        self.img_upload.name = valid_filename
        super(ImagePortfolio, self).save(*args, **kwargs)
 