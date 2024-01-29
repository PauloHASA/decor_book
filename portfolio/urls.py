
from django.urls import path, include
from . import views

app_name = "portfolio"

urlpatterns = [
    path('', views.timeline_portfolio, name='timeline_portfolio'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/store_portfolio/', views.store_portfolio, name='store_portfolio'),
    path('portfolio/product_page/', views.produt_page, name='product_page'),
]
