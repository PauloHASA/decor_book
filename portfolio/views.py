from django.shortcuts import render

# Create your views here.

def timeline_portfolio(request):
    return render(request,'timeline_portfolio.html')

def portfolio(request):
    return render(request,'portfolio.html')

def store_portfolio(request):
    return render(request,'store-portfolio.html')

def produt_page(request):
    return render(request,'product-page.html')
