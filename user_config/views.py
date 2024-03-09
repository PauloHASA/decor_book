from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, LoginUserForm, ClientForm, ProfessionalForm
from .models import CustomUserModel, ClientProfile, ProfessionalProfile
from django.contrib import messages
from .controllers import FolderUserPost, CustomFormErrors
from django_require_login.decorators import public


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