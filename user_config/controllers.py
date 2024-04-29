import os 
from django.conf import settings
from datetime import datetime


class FolderUserPost:
    @staticmethod
    def create_user_folder(user_id):
        users_folder_path = os.path.join(settings.MEDIA_ROOT, "users_folder")
        if not os.path.exists(users_folder_path):
            os.makedirs(users_folder_path)
            
        user_folder = os.path.join(users_folder_path, str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        return user_folder
            
    @staticmethod
    def create_post_folder(user_id, post_id):
        user_folder = FolderUserPost.create_user_folder(user_id)
        post_folder = os.path.join(user_folder, str(post_id))
        if not os.path.exists(post_folder):
            os.makedirs(post_folder)
            
        print('-'*100)
        print('Folder path: ',post_folder)
        print('-'*100)

        return post_folder


    @staticmethod
    def image_filename(instance, filename):
        user_id = instance.new_project.user.id
        post_id = instance.new_project.id
        user_folder = FolderUserPost.create_user_folder(user_id)
        post_folder = FolderUserPost.create_post_folder(user_id, post_id)
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        filepath = f"users_folder/{user_id}/{post_id}//img_{timestamp}_{filename}"
        
        print("Caminho da imagem:", filepath) 
        return filepath


    def user_folder_path(user_id):
        users_folder_path = os.path.join(settings.MEDIA_ROOT, "users_folder")
        user_folder = os.path.join(users_folder_path, str(user_id))
        return user_folder


class CustomFormErrors:
    
    def get_email_error(form):
        return form.errors.get('email', None)
    
    def get_username_error(form):
        return form.errors.get('user_name', None)
    
    def get_password_error(form):
        return form.errors.get('password2', None)