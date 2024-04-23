from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.forms.models import model_to_dict
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime

from .forms import FormStepOne, FormStepTwo, FormStepThree, FormStepTwoOverwrite
from .models import NewProject, ImagePortfolio
from .controller import create_save_session

from user_config.models import ProfessionalProfile, CustomUserModel
from user_config.controllers import FolderUserPost


import random

# Create your views here.

def my_projects(request):
    return render(request,'my-projects.html')


def portfolio(request):
    return render(request,'portfolio.html')


def store_portfolio(request):
    return render(request,'store_portfolio.html')


def home_page(request):
    user = request.user  
    is_authenticated = user.is_authenticated
    if is_authenticated:
        is_superuser = user.is_superuser
        
        if not is_superuser:
            try:
                professional_profile = ProfessionalProfile.objects.get(user=user)
                is_professional = professional_profile.is_professional
            except ProfessionalProfile.DoesNotExist:
                is_professional = False
                
        show_button = is_superuser or is_professional
    else:
        show_button = False
    
    return render(request, 'home-page.html', {'user': user,
                                              'show_button': show_button,
                                              })


def new_project_step1(request): 
    form = FormStepOne()
    if request.method == 'POST':
        form = FormStepOne(request.POST)
        
        if form.is_valid():
            step_one_data = form.save(commit=False)
            step_one_data.data_initial = step_one_data.data_initial.strftime('%Y-%m-%d')
            step_one_data.data_final = step_one_data.data_final.strftime('%Y-%m-%d')
            
            cleaned_data_dic = model_to_dict(step_one_data)
            request.session['step_one_data']= cleaned_data_dic

            return redirect('portfolio:new_project_step2')
        else:
            form = FormStepOne()
            print('Formulario não é valido')

            
    return render(request,'new-project-step1.html', {'form_stepone':form})


def new_project_step2(request):
    if 'step_one_data' not in request.session:
        return redirect('portfolio:new_project_step1')
    
    form = FormStepTwo()

    if request.method == 'POST':
        form = FormStepTwoOverwrite(request.POST)
        if form.is_valid():
            step_two_data = form.save(commit=False)
            cleaned_data_dic = model_to_dict(step_two_data)


            request.session['step_two_data']= form.cleaned_data
            return redirect('portfolio:new_project_step3')
        else:
            form = FormStepTwo()
            
    return render(request,'new-project-step2.html', {'form_steptwo':form})


@transaction.atomic
def new_project_step3(request):
    if 'step_two_data' not in request.session or 'step_one_data' not in request.session:
        return redirect('portfolio:new_project_step2')
    
    form_step_one = FormStepOne(request.session['step_one_data'])
    form_step_two = FormStepTwo(request.session['step_two_data'])
    form_step_three = FormStepThree()

    if request.method == 'POST':
        form_step_three = FormStepThree(request.POST, request.FILES)
        if form_step_one.is_valid() and form_step_two.is_valid() and form_step_three.is_valid():
            new_project = create_save_session(request, request.session['step_one_data'], request.session['step_two_data'])
            new_project.user = request.user
            new_project.data_initial = form_step_one.cleaned_data['data_initial']
            new_project.data_final = form_step_one.cleaned_data['data_final']
            new_project.area = form_step_two.cleaned_data['area']
            new_project.rooms = form_step_two.cleaned_data['rooms']
            new_project.style = form_step_two.cleaned_data['style']
            new_project.categories = form_step_two.cleaned_data['categories']
            new_project.add_stores = form_step_two.cleaned_data['add_stores']
            new_project.save()
                        
            # Processar imagens
            images = request.FILES.getlist('img_upload')
            for image in images:
                ImagePortfolio.objects.create(img_upload=image, new_project=new_project)

                
            # Criar pasta para o post
            FolderUserPost.create_post_folder(new_project.user.id, new_project.id)
            
            # Limpar dados da sessão
            del request.session['step_one_data']
            del request.session['step_two_data']
            
            return JsonResponse({'status': 'success'})
        else:
            print("Erros em form_step_three:", form_step_three.errors)
    else:
        form_step_three = FormStepThree()
    
    return render(request, 'new-project-step3.html', {'form_stepthree': form_step_three})


def timeline_portfolio(request):
    projects = NewProject.objects.select_related('user').prefetch_related('imageportfolio_set').all()    
    for project in projects:
        project.images = list(project.imageportfolio_set.all().order_by('?'))  
    return render(request, 'timeline_portfolio.html', {'projects': projects})


def project_page(request, project_id):
    project = get_object_or_404(NewProject, pk=project_id)
    
    area = project.area
    data_final_ano = project.data_final.year
    username = project.user.full_name
    name = project.name
    summary = project.summary
    style = project.style
    partner = project.partner
    images = project.imageportfolio_set.all()
    
    user = project.user
    
    if user.is_authenticated and user.is_professional:
        try:
            professional_profile = ProfessionalProfile.objects.get(user=user)
            profession = professional_profile.profession
        except ProfessionalProfile.DoesNotExist:
            profession = ""
    
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
    }
    return render(request,'project-page.html', context)


def lobby_payment(request):
    return render(request, "lobby-payment.html")


def payment_page(request):
    return render(request, "payment-page.html")