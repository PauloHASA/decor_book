from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, LoginUserForm
from django.contrib import messages
from .controllers import FolderUserPost, CustomFormErrors

# Create your views here.

def register_page(request):
    form = UserRegistrationForm()
    email_errors = None
    username_errors = None
    password_errors = None
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            createfolder = FolderUserPost.create_user_folder(user.id)
            return redirect("user:login")
        else:
            email_errors = CustomFormErrors.get_email_error(form)
            username_errors = CustomFormErrors.get_username_error(form)
            password_errors = CustomFormErrors.get_password_error(form)
            form = UserRegistrationForm()
            
    return render( request,
                  'register.html', 
                  {'form':form, 
                   'email_errors':email_errors, 
                   'username_errors':username_errors, 
                   'password_errors':password_errors, 
                   }
                  )


def login_page(request):
        
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect(" portfolio:home_page")
            else:
                form = LoginUserForm()
                error_message =  " Invalid credentials. Please, try again."
                return render(request,
                              "login.html",
                              {"error_message":error_message, "login_form":form},
                              )
    form = LoginUserForm()
    return render(request,
                    "login.html",
                    {"login_form":form},
                    )

def logout_view(request):
    logout(request)
    return redirect('user:landing_page')

def landing_page(request):
    return render(request, "landing_page.html")