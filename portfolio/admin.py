from django.contrib import admin
from .models import NewProject,  ImagePortfolio

# Register your models here.


class NewProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_name', 'user_email')
    
    def full_name(self, obj):
        return obj.user.full_name
    
    def user_email(self, obj):
        return obj.user.email


class ImagePortifolioAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user_email', 'new_project_name', 'categories_name')
    
    def new_project_name(self, obj):
        return obj.new_project.name
    
    def categories_name(self, obj):
        return obj.new_project.categories
    
    def full_name(self, obj):
        return obj.new_project.user.full_name
    
    def user_email(self, obj):
        return obj.new_project.user.email
        

admin.site.register(NewProject, NewProjectAdmin)
admin.site.register(ImagePortfolio, ImagePortifolioAdmin)
