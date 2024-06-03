
from django.urls import path
from . import views

app_name = "campaigns"

urlpatterns = [
    path('send_email/', views.send_test_email, name='send_email'),
    path('email_build/', views.email_build, name='email_build'),
    path('main/', views.main, name='main'),
]

