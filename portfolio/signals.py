from django.db.models.signals import pre_delete
from django.dispatch import receiver
from portfolio.models import NewProject
from user_config.controllers import FolderUserPost
import shutil


@receiver(pre_delete, sender=NewProject)
def delete_project_files(sender, instance, **kwargs):
    folder_path = FolderUserPost.user_folder_path(instance.user.id)
    shutil.rmtree(folder_path)