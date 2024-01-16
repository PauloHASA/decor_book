
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.timeline_portfolio, name='timeline_portfolio.html'),
]
