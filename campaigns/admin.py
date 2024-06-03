from django.contrib import admin
from .models import Dataframe

@admin.register(Dataframe)
class DataframeAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'user','admin_id', 'name', 'latitude', 'longitude', 'coord_geoc', 'email']
    list_display_links = ['request_id', 'user','admin_id', 'name']
    
    
    

