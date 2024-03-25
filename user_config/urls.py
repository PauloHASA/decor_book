
from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register_page/', views.register_page, name='register-page'),
    
    path('register-client/', views.register_client, name='register-client'),
    path('register_professional/', views.register_professional, name='register-professional'),
    path('register_company/', views.register_company, name='register-company'),
    
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('professional_profile/<int:profile_id>/', views.professional_profile, name='professional_profile'),
    path('profile/', views.profile, name='profile'),
]
