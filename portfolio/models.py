from django.db import models
from django.core.exceptions import ValidationError
from user_config.models import CustomUserModel
from user_config.controllers import FolderUserPost
# Create your models here.


class NewProject(models.Model):
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    partner = models.CharField(max_length=150)
    summary = models.TextField()
    data_initial = models.DateField(null=True)
    data_final= models.DateField(null=True)
    area = models.CharField(max_length=150)
    rooms = models.CharField(max_length=150)
    style = models.CharField(max_length=150)
    categories = models.CharField(max_length=150)
    add_stores = models.CharField(max_length=150)
    
    def clean(self):
        if self.data_final is not None and self.data_initial is not None:
            if self.data_final < self.data_initial:
                raise ValidationError("A data final não pode ser anterior á data inicial.")

class ImagePortfolio(models.Model):
    new_project = models.ForeignKey(NewProject, on_delete=models.CASCADE)
    img_upload = models.ImageField(upload_to=FolderUserPost.image_filename)
 