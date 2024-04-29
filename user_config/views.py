from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .models import CustomUserModel, ClientProfile, ProfessionalProfile
from .controllers import FolderUserPost, CustomFormErrors
from .forms import UserRegistrationForm, LoginUserForm, ClientForm, ProfessionalForm, ProfileEditForm

from portfolio.models import NewProject, ImagePortfolio


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
            user.save()
            professional_profile = ProfessionalProfile.objects.create(user=user, profession=profession, site=site)
            createfolder = FolderUserPost.create_user_folder(user.id)
            return redirect('user:login')
        else:
            print(form.errors)
            return render(request, 'register-professional.html', {'form':form})
    else:
        form = ProfessionalForm()
    return render( request, 'register-professional.html',{'form':form})


def register_company(request):
    return render(request, "register-company.html")
 
 
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
                              {"error_message":error_message, "login_form":form},
                              )
        else:
            print(form.errors)
            return render(request, "login.html", {"login_form":form} )
    return render(request, "login.html", {"login_form":form} )


def logout_view(request):
    logout(request)
    return redirect('user:landing_page')


def landing_page(request):
    return render(request, "landing_page.html")



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
            
    
    context = {'profile': profile,
               'first_project_image': first_project_image,
               'projects': projects
               }
        
        
    return render(request, "professional_profile.html", context)



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
    
    context = {
        'profile': profile,
        'first_project_image': first_project_image,
        'projects': projects,
        'edit_profile_form': edit_profile_form, 
    }
    
    return render(request, "profile_professional.html", context)


@login_required
def save_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user:profile_professional')  # Redireciona para a página de perfil após salvar
        else:
            # Se o formulário não for válido, você pode lidar com isso aqui
            # Por exemplo, pode renderizar o mesmo template com o formulário e exibir mensagens de erro
            # Ou redirecionar para uma página de erro
            pass
    else:
        # Se não for uma solicitação POST, você pode redirecionar para a página de perfil ou fazer outra coisa
        pass


