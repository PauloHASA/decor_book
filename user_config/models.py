from django.db import models


# Create your models here.

class ClientModel(models.Model):
    fullname = models.CharField(max_length=300, null=False)
    email = models.TextField(null=False)
    profession = models.EmailField(null=False)


class ProfessionModal(models.Model):
    ...
    

class CompanyModel(models.Model):
    ...