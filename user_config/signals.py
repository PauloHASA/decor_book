from django.db.models.signals import pre_delete
from django.dispatch import receiver
import shutil

from .controllers import FolderUserPost
from .models import CustomUserModel
from portfolio.models import NewProject

@receiver(pre_delete, sender=CustomUserModel)
def delete_user_folders(sender, instance, **kwargs):
    user_posts = NewProject.objects.filter(author=instance)
    for post in user_posts:
        post = FolderUserPost.user_folder_path(instance.id)
        shutil.rmtree(post, ignore_errors=True)