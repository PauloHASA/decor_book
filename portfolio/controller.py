from .models import NewProject, ImagePortfolio
from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _



def create_save_session(request, step_one_data, step_two_data):
    step_one_cleaned = {key: value for key, value in step_one_data.items() if value is not None and value != ''}
    step_two_cleaned = {key: value for key, value in step_two_data.items() if value is not None and value != ''}
    
    project_data = {**step_one_cleaned, **step_two_cleaned}
    
    if 'partner' not in project_data:
        project_data['partner'] = ''
        
    if 'area' not in project_data:
        project_data['area'] = ''
        
    if 'rooms' not in project_data:
        project_data['rooms'] = ''
        
    if 'style' not in project_data:
        project_data['style'] = ''
        
    if 'categories' not in project_data:
        project_data['categories'] = ''
        
    if 'add_stores' not in project_data:
        project_data['add_stores'] = ''
            
    project_data['user'] = request.user
    
    new_project = NewProject(**project_data)
    
    images = request.FILES.getlist('img_upload')
    if not images:
        return None
    
    new_project.save()
    
    # for image in images:
    #     ImagePortfolio.objects.create(img_upload=image, new_project=new_project)
    
    return new_project
