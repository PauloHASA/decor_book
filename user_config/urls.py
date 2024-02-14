
from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
