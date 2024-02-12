from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterClientForm, LoginForm

# Create your views here.

def register_page(request):
    form = RegisterClientForm()

    if request.method == 'POST':
        form = RegisterClientForm(request.POST)
        if form.is_valid():
            form.save()
            print("cheguei aqui 3")

            return redirect ('user:login')
        else:
            form = RegisterClientForm()
        return render(request, 'register.html',{'form':form})
    return render( request, 'register.html', {'form':form})


def login_page(request):
    if request.method == 'POST':
        print("cheguei aqui 1")

        form = LoginForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                print("cheguei aqui 2")
                return redirect("portifolio:timeline_portfolio")
    else:
        form = LoginForm()
    return render( request, 'login.html', {'form':form})


def logout_view(request):
    logout(request)
    return redirect('login.html')