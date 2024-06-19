from django.core.files.storage import FileSystemStorage
from pathlib import Path

class UserImageStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = Path(__file__).resolve().parent.parent.parent / 'projects_images' / 'upload_files'
        super().__init__(*args, **kwargs)