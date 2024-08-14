from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django_require_login.decorators import public
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_control

from .models import (CustomUserModel, 
                     ClientProfile, 
                     ProfessionalProfile,
                     CompanyProfile,
                     )
from .controllers import (FolderUserPost, 
                          CustomFormErrors,
                          )
from .forms import (UserRegistrationForm, 
                    LoginUserForm, 
                    ClientForm, 
                    ProfessionalForm, 
                    ProfileEditForm, 
                    ProfessionalProfileForm, 
                    CompanyForm,
                    )
from portfolio.models import (NewProject, 
                              ImagePortfolio,
                              )

from .forms import PaymentForm
from api_pagbank.api_pagbank import payment_card
from django.http import JsonResponse


def register_page(request):
    return render(request, "register-page.html")

def register_professional(request):
    if request.method == 'POST':
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            site = form.cleaned_data['site']
            profession = form.cleaned_data['profession']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2'] 
            
            if password1 != password2:
                return render(request, 'register-professional.html', {'form': form, 'error': 'As senhas não coincidem' })

            user = CustomUserModel.objects.create_user(email=email,
                                                       user_name=email,
                                                       full_name=full_name,
                                                       password=password1)
            user.is_professional = True
            
            source = request.GET.get('source')
            if source == 'marketing':
                user.is_marketing = True
            else:
                user.is_organic = True
            
            user.save()
            
            professional_profile = ProfessionalProfile.objects.create(user=user, 
                                                                      profession=profession, 
                                                                      site=site
                                                                      )
            
            createfolder = FolderUserPost.create_user_folder(user.id)
            return redirect('user:login')
        else:
            print(form.errors)
            return render(request, 'register-professional.html', {'form':form})
    else:
        form = ProfessionalForm()
    return render( request, 'register-professional.html',{'form':form})


def register_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            try:
                form.is_active = True
                form.is_paid = False
                form.is_company = True
                form.save()
                
                return redirect('user:login')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = CompanyForm()
    return render(request, "register-company.html", {'form':form})
 

def register_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            full_name = form.cleaned_data['full_name']
            profession = form.cleaned_data['profession']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                return render(request, 'register-client.html', {'form': form, 'error': 'As senhas não coincidem' })

            user = CustomUserModel.objects.create_user(email=email,
                                                       user_name=email,
                                                       full_name=full_name,
                                                       password=password1)
            user.is_client = True
            user.save()
            cliente_profile = ClientProfile.objects.create(user=user, profession=profession)
            createfolder = FolderUserPost.create_user_folder(user.id)
            return redirect("user:login")
        else:
            print(form.errors)
            return render(request, 'register-client.html', {'form':form})
    else:
        form = ClientForm()
    return render( request, 'register-client.html',{'form':form})
   

def login_page(request):
    form = LoginUserForm()

    if request.method == "POST":
        form = LoginUserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect("portfolio:home_page")
            else:
                form = LoginUserForm()
                error_message =  " Invalid credentials. Please, try again."
                return render(request,
                              "login.html",
                              {"error_message":error_message,
                               "login_form":form,
                               },
                              )
        else:
            print(form.errors)
            return render(request, "login.html", {"login_form":form} )
    return render(request, "login.html", {"login_form":form} )


def logout_view(request):
    logout(request)
    return redirect('user:landing_page')


@cache_control(max_age=3600)
def landing_page(request):
    projects = NewProject.objects.select_related('user').prefetch_related('imageportfolio_set').all()    
    for project in projects:
        project.images = list(project.imageportfolio_set.all().order_by('?'))
        
    response = render(request, 'timeline_portfolio.html', {'projects': projects})
    patch_cache_control(response, max_age=3600)
    
    context = {
                'projects': projects,
                }

    return render(request, "landing_page.html", context)


@login_required
def professional_profile(request, profile_id):
    profile_user = get_object_or_404(CustomUserModel, pk=profile_id)
    profile = get_object_or_404(ProfessionalProfile, user=profile_user)
    projects = NewProject.objects.filter(user=profile_user)
    first_project_image = None
    
    if projects.exists():
        first_project = projects.first()
        first_project_image = ImagePortfolio.objects.filter(new_project=first_project)
        if first_project_image.exists():
            first_project_image = first_project_image.first().img_upload.url
            
    print(profile.profile_picture.url)
    
    context = {'profile': profile,
               'profile_picture_url': profile.profile_picture.url if profile.profile_picture else None,
               'first_project_image': first_project_image,
               'projects': projects
               }
        
        
    return render(request, "professional_profile.html", context)

@login_required
def profile_client(request):
    user = request.user
    
    profile = get_object_or_404(ClientProfile, user=user)
    
    projects = NewProject.objects.filter(user=user)
    first_project_image = None
    
    if projects.exists():
        first_project = projects.first()
        first_project_image = ImagePortfolio.objects.filter(new_project=first_project)
        if first_project_image.exists():
            first_project_image = first_project_image.first().img_upload.url
            
    
    context = {'profile': profile,
               'first_project_image': first_project_image,
               'projects': projects
               }
        
        
    return render(request, "profile_client.html", context)


@login_required
def profile_professional(request):
    user = request.user
    profile = get_object_or_404(ProfessionalProfile, user=user)
    projects = NewProject.objects.filter(user=user)
    first_project_image = None
    
    if projects.exists():
        first_project = projects.first()
        first_project_image = ImagePortfolio.objects.filter(new_project=first_project)
        if first_project_image.exists():
            first_project_image = first_project_image.first().img_upload.url
    
    edit_profile_form = ProfileEditForm(instance=user)  
    edit_profile_picture = ProfessionalProfileForm()  
    
    modal_open = request.GET.get('modal_open', 'false') == 'true'
    
    print(profile.profile_picture.url)

    
    context = {
        'profile': profile,
        'profile_picture_url': profile.profile_picture.url if profile.profile_picture else None,
        'first_project_image': first_project_image,
        'projects': projects,
        'edit_profile_form': edit_profile_form, 
        'edit_profile_picture': edit_profile_picture,
        'modal_open':modal_open,
    }
    
    
    return render(request, "profile_professional.html", context)


@login_required
def save_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        profile_form = ProfessionalProfileForm(request.POST, request.FILES, instance=request.user.professional_profile)

        if form.is_valid() and profile_form.is_valid():
            print('Formulario valido')
            user_form = form.save(commit=False)
            profile_form_instance = profile_form.save(commit=False)
            user_form.save()
            profile_form_instance.user = request.user
            profile_form_instance.save()
            return redirect('user:profile_professional')  
        else:
            user = request.user
            profile = get_object_or_404(ProfessionalProfile, user=user)
            projects = NewProject.objects.filter(user=user)
            first_project_image = None
            
            if projects.exists():
                first_project = projects.first()
                first_project_image = ImagePortfolio.objects.filter(new_project=first_project)
                if first_project_image.exists():
                    first_project_image = first_project_image.first()
            
            context = {
                'profile': profile,
                'first_project_image':first_project_image,
                'projects':projects,
                'edit_profile_form': form,  
                'edit_profile_picture': profile_form,  
                'modal_open': True 
            }
            
            return render(request, "profile_professional.html", context)


@login_required
def load_header(request):
    try:
        user = request.user
        if user.is_authenticated and user.is_company:
            company_profile = CompanyProfile.objects.get(user=user)
            fantasy_name = company_profile.fantasy_name
        else:
            fantasy_name = None
    except CompanyProfile.DoesNotExist:
        fantasy_name = None
    
    context = {
        'fantasy_name':fantasy_name,
    }
    
    return render(request, 'header.html', context )



def payment_view(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Coleta os dados do formulário
            data = form.cleaned_data
            encrypted_card = request.POST.get('encrypted_card')

            # Chama a função para criar o pagamento
            response = payment_card(
                encrypted_card=encrypted_card,
                name=data['name'],
                email=data['email'],
                tax_id=data['tax_id'],
                phone=data['phone'],
                item_name=data['item_name'],
                amount=data['amount']
            )
            
            # Trata a resposta da API do PagBank
            if 'error' in response:
                return JsonResponse({'error': response['error']}, status=500)
            return JsonResponse(response)
    else:
        form = PaymentForm()

    return render(request, 'payment_test.html', {'form': form})