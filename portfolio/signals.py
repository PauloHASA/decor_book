import shutil
import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from portfolio.models import NewProject
from user_config.controllers import FolderUserPost


@receiver(pre_delete, sender=NewProject)
def delete_project_files(sender, instance, **kwargs):
    folder_path = FolderUserPost.user_folder_path(instance.user.id)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)