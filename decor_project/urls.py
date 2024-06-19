"""
URL configuration for decor_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_config.urls'), name='user_config'),
    path('portfolio/', include('portfolio.urls'), name='portfolio'),
    path('campaigns/', include('campaigns.urls'), name='campaigns'),
    
    path('accounts/', include('allauth.urls')),
    
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': os.environ.get('CUSTOM_MEDIA_ROOT') ,}),
]
