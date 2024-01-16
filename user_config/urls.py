
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('user-register/', views.user_register, name='user_register'),
]
