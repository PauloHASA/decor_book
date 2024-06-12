from .models import NewProject
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _



def create_save_session(request, step_one_data, step_two_data):
    step_one_cleaned = {key: value for key, value in step_one_data.items() if value is not None and value != ''}
    step_two_cleaned = {key: value for key, value in step_two_data.items() if value is not None and value != ''}
    
    project_data = {**step_one_cleaned, **step_two_cleaned}
    
    if 'partner' not in project_data:
        project_data['partner'] = ''
        
    project_data['user'] = request.user
    
    new_project = NewProject.objects.create(**project_data)
    
    return new_project
