
from django.urls import path
from . import views

app_name = "campaigns"

urlpatterns = [
    path('send_email/', views.send_test_email, name='send_email'),
    path('email_welcome/', views.email_welcome, name='email_welcome'),
    path('email_marketing/', views.email_marketing, name='email_marketing'),
    
]

