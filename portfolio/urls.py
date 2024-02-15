
from django.urls import path
from . import views

app_name = " portfolio"

urlpatterns = [
    path("", views.timeline_portfolio, name="timeline_portfolio"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("my-projects/", views.my_projects, name="my_projects"),
    path("store_portfolio/", views.store_portfolio, name="store_portfolio"),
    path("project_page/", views.project_page, name="project_page"),
    
    path("home_page/", views.home_page, name="home_page"),
    path("new_project_step1/", views.new_project_step1, name="new_project_step1"),
    path("new_project_step2/", views.new_project_step2, name="new_project_step2"),
    path("new_project_step3/", views.new_project_step3, name="new_project_step3"),
    
]
