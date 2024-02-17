from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, LoginUserForm
from django.contrib import messages

# Create your views here.

def register_page(request):
    form = UserRegistrationForm()
    print('View Function')
    if request.POST:
        print('form register')

        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print('is valid')

            form.save()
            HttpResponse("Deu certo")
            return redirect("user:login")
        else:
            form = UserRegistrationForm()
            HttpResponse("não rolou")

                
    return render( request, 'register.html', {'form':form})


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
    return redirect('user:login')