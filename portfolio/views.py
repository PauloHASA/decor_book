from django.shortcuts import render, redirect, HttpResponse
from django.forms.models import model_to_dict
from datetime import datetime

from .forms import FormStepOne, FormStepTwo, FormStepThree, FormStepTwoOverwrite
from .models import NewProject, ImagePortfolio
from .controller import create_save_session

# Create your views here.

def timeline_portfolio(request):
    return render(request,'timeline_portfolio.html')

def my_projects(request):
    return render(request,'my-projects.html')

def portfolio(request):
    return render(request,'portfolio.html')

def store_portfolio(request):
    return render(request,'store_portfolio.html')

def project_page(request):
    return render(request,'project-page.html')

def home_page(request):
    return render(request,'home-page.html')

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
            
            print('-'*100)
            print(cleaned_data_dic)
            print('-'*100)
            
            return redirect(' portfolio:new_project_step2')
        else:
            form = FormStepOne()
            print('Formulario não é valido')

            
    return render(request,'new-project-step1.html', {'form_stepone':form})

def new_project_step2(request):
    if 'step_one_data' not in request.session:
        return redirect(' portfolio:new_project_step1')
    
    form = FormStepTwo()

    if request.method == 'POST':
        form = FormStepTwoOverwrite(request.POST)
        if form.is_valid():
            step_two_data = form.save(commit=False)
            cleaned_data_dic = model_to_dict(step_two_data)

            print(' '*100)
            print('-'*100)
            print(cleaned_data_dic)
            print('-'*100)
            print(' '*100)

            request.session['step_two_data']= form.cleaned_data
            return redirect(' portfolio:new_project_step3')
        else:
            form = FormStepTwo()
            
    return render(request,'new-project-step2.html', {'form_steptwo':form})


def new_project_step3(request):
    if 'step_two_data' not in request.session or 'step_one_data' not in request.session:
        return redirect(' portfolio:new_project_step2')
    
    form_step_one = FormStepOne(request.session['step_one_data'])
    form_step_two = FormStepTwo(request.session['step_two_data'])

    
    if request.method == 'POST':
        form_step_three = FormStepThree(request.POST, request.FILES)
        print('Method post')
        if form_step_one.is_valid() and form_step_two.is_valid() and form_step_three.is_valid():
            # Criar um novo projeto com dados dos formulários da etapa 1 e 2
            print('formulario valido')

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
            
            print(new_project)
            
            # Processar imagens
            images = request.FILES.getlist('img_upload')
            for image in images:
                ImagePortfolio.objects.create(img_upload=image, new_project=new_project)
                
            # Limpar dados da sessão
            del request.session['step_one_data']
            del request.session['step_two_data']
            
            return redirect(" portfolio:timeline_portfolio")

        else:
            print("Erros em form_step_three:", form_step_three.errors)
            

        
    else:
        form_step_three = FormStepThree()

    return render(request, 'new-project-step3.html', {'form_stepthree': form_step_three})
