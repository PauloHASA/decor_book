from django.shortcuts import render

# Create your views here.

def login_page(request):
    return render( request, 'login_page.html')

def user_register(request):
    return render( request, 'user_register.html')