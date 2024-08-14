from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.text import get_valid_filename
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from datetime import datetime

from .forms import FormStepOne, FormStepTwo, FormStepThree, FormStepTwoOverwrite
from .models import NewProject, ImagePortfolio
from .controller import create_save_session
from .tasks import process_image_upload

from user_config.models import ProfessionalProfile, CustomUserModel
from user_config.controllers import FolderUserPost

import random
import logging
import os

logger = logging.getLogger('myapp')
import logging
import os

logger = logging.getLogger('myapp')


@login_required
def my_projects(request):
    return render(request,'my-projects.html')


@login_required
def portfolio(request):
    return render(request,'portfolio.html')


@login_required
def store_portfolio(request):
    return render(request,'store_portfolio.html')


@login_required
def home_page(request):
    user = request.user  
    is_authenticated = user.is_authenticated
    if is_authenticated:
        is_superuser = user.is_superuser
        
        if not is_superuser:
            try:
                professional_profile = ProfessionalProfile.objects.get(user=user)
                is_professional = professional_profile.is_professional
                is_paid = user.is_paid

            except ProfessionalProfile.DoesNotExist:
                is_professional = False
                is_paid = False
                
        show_button = is_superuser or is_professional or is_paid
    else:
        show_button = False
    
    return render(request, 'home-page.html', {'user': user,
                                              'show_button': show_button,
                                              })


@login_required
def new_project_step1(request): 
    form = FormStepOne(request.POST or None)
    if form.is_valid():
        step_one_data = form.save(commit=False)
        if step_one_data.data_initial:
            step_one_data.data_initial = step_one_data.data_initial.strftime('%Y-%m-%d')
        if step_one_data.data_final:
            step_one_data.data_final = step_one_data.data_final.strftime('%Y-%m-%d')
        
        cleaned_data_dic = model_to_dict(step_one_data)
        request.session['step_one_data'] = cleaned_data_dic

        return redirect('portfolio:new_project_step2')
            
    return render(request, 'new-project-step1.html', {'form_stepone': form})


@login_required
def new_project_step2(request):
    if 'step_one_data' not in request.session:
        return redirect('portfolio:new_project_step1')
    
    form = FormStepTwo(request.POST or None)
    if form.is_valid():
        step_two_data = form.save(commit=False)
        cleaned_data_dic = model_to_dict(step_two_data)

        request.session['step_two_data'] = cleaned_data_dic
        return redirect('portfolio:new_project_step3')
           
    return render(request, 'new-project-step2.html', {'form_steptwo': form})


@login_required
@transaction.atomic
def new_project_step3(request):
    logger.info("Starting new_project_step3 view with method: %s", request.method)
    
    logger.info("Starting new_project_step3 view with method: %s", request.method)
    
    if not request.session.get('step_one_data') or not request.session.get('step_two_data'):
        logger.warning("Session data missing for step one or step two")
        logger.warning("Session data missing for step one or step two")
        return redirect('portfolio:new_project_step2')
    
    form_step_three = FormStepThree(request.POST, request.FILES or None)
    logger.info("FormStepThree initialized")

    if request.method == 'POST':
        logger.info("POST method detected")
        
        if form_step_three.is_valid():
            logger.info("Form is valid")
            new_project = create_save_session(request, request.session['step_one_data'], request.session['step_two_data'])
            
            if new_project is None:
                logger.error("Failed to create new project - No associated images")
                return HttpResponse("Erro: É necessário associar imagens ao projeto.")
            
            new_project.user = request.user
            new_project.save()
            logger.info(f"New project saved with id {new_project.id}")
                        
            images = request.FILES.getlist('img_upload')
            
            for image in images:
                file_name = image.name
                valid_filename = get_valid_filename(file_name)
                image.name = valid_filename
                
                image_instance = ImagePortfolio(img_upload=image, new_project=new_project)
                image_instance.save()
                                
                process_image_upload.delay(image_instance.id)
                logger.info(f"Image {image.name} saved for project {new_project.id}")

            FolderUserPost.create_post_folder(new_project.user.id, new_project.id)
            logger.info(f"Post folder created for user {new_project.user.id} and project {new_project.id}")
            
            del request.session['step_one_data']
            del request.session['step_two_data']
            logger.debug("Session data deleted")
            
            return redirect('portfolio:project_page', project_id=new_project.id)
        else:
            logger.warning("Form is not valid")
            FolderUserPost.create_post_folder(new_project.user.id, new_project.id)
            logger.info(f"Post folder created for user {new_project.user.id} and project {new_project.id}")
            
            del request.session['step_one_data']
            del request.session['step_two_data']
            logger.debug("Session data deleted")
            
            return redirect('portfolio:project_page', project_id=new_project.id)
   
    return render(request, 'new-project-step3.html', {'form_stepthree': form_step_three})

@login_required
@cache_control(max_age=3600)
def timeline_portfolio(request):

    projects = NewProject.objects.select_related('user').prefetch_related('imageportfolio_set').all()    
    for project in projects:
        project.images = list(project.imageportfolio_set.all().order_by('?'))
    
    context = {
        'projects': projects,
        }
    
    response = render(request, 'timeline_portfolio.html', context)
    patch_cache_control(response, max_age=3600)
    return response

@login_required

def project_page(request, project_id):
    project = get_object_or_404(NewProject, pk=project_id)
    
    area = project.area
    
    if project.data_final is not None:        
        data_final_ano = project.data_final.year
    else:
        data_final_ano = ''
        
    username = project.user.full_name
    name = project.name
    summary = project.summary
    style = project.style
    partner = project.partner
    images = project.imageportfolio_set.all()
    
    user = project.user
    name = user.full_name
    
    user = project.user
    profession = ""
    if user.is_authenticated and user.is_professional:
        try:
            professional_profile = ProfessionalProfile.objects.get(user=user)
            profession = professional_profile.profession
        except ProfessionalProfile.DoesNotExist:
            pass
    
    is_owner = request.user == project.user
    
    context = {
        'project': project,
        'images': images,
        'area': area,
        'profession': profession,
        'summary': summary,
        'data_final_ano': data_final_ano,
        'partner':partner,
        'name': name,
        'username': username,
        'style': style,
        'name': name,
        'is_owner': is_owner,
    }
    return render(request,'project-page.html', context)


def project_page_pub(request, project_id):
    project = get_object_or_404(NewProject, pk=project_id)
    
    area = project.area
    
    if project.data_final is not None:        
        data_final_ano = project.data_final.year
    else:
        data_final_ano = ''
    
    username = project.user.full_name
    name = project.name
    summary = project.summary
    style = project.style
    partner = project.partner
    images = project.imageportfolio_set.all()
    
    user = project.user
    name = user.full_name
    
    user = project.user
    profession = ""
    if user.is_authenticated and user.is_professional:
        try:
            professional_profile = ProfessionalProfile.objects.get(user=user)
            profession = professional_profile.profession
        except ProfessionalProfile.DoesNotExist:
            pass
    
    context = {
        'project': project,
        'images': images,
        'area': area,
        'profession': profession,
        'summary': summary,
        'data_final_ano': data_final_ano,
        'partner':partner,
        'name': name,
        'username': username,
        'style': style,
        'name': name
    }
    return render(request,'project-page-pub.html', context)


def lobby_payment(request):
    return render(request, "lobby-payment.html")


def payment_page(request):
    return render(request, "payment-page.html")


@login_required
def client_property(request):
    return render(request, "client-property.html")


@login_required
def hunter_douglas(request):
    return render(request, "hunter_douglas.html")


def new_project_page(request, project_id):
    project = get_object_or_404(NewProject, pk=project_id)
    
    area = project.area
    
    if project.data_final is not None:        
        data_final_ano = project.data_final.year
    else:
        data_final_ano = ''
        
    username = project.user.full_name
    name = project.name
    summary = project.summary
    style = project.style
    partner = project.partner
    images = project.imageportfolio_set.all()
    
    user = project.user
    name = user.full_name
    
    user = project.user
    profession = ""
    if user.is_authenticated and user.is_professional:
        try:
            professional_profile = ProfessionalProfile.objects.get(user=user)
            profession = professional_profile.profession
        except ProfessionalProfile.DoesNotExist:
            pass
    
    is_owner = request.user == project.user
    
    context = {
        'project': project,
        'images': images,
        'area': area,
        'profession': profession,
        'summary': summary,
        'data_final_ano': data_final_ano,
        'partner':partner,
        'name': name,
        'username': username,
        'style': style,
        'name': name,
        'is_owner': is_owner,
    }

    return render(request, "new-project-page.html", context)