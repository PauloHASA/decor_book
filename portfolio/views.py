from django.shortcuts import render

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
    return render(request,'new-project-step1.html')

def new_project_step2(request):
    return render(request,'new-project-step2.html')

def new_project_step3(request):
    return render(request,'new-project-step3.html')
