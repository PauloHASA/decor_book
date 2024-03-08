from django.contrib import admin
from .models import CustomUserModel, ClientProfile, ProfessionalProfile, ConstructionProfile
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'user_name',)
    list_filter = ('email', 'user_name',
                    'is_active', 'is_staff', 'is_superuser' )
    ordering = ('-start_date',)
    list_display = ('id', 'email', 'user_name',
                    'is_active', 'is_staff', 'is_superuser')
    list_display_links = ['id', 'email', 'user_name',]
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'full_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        CustomUserModel.about: {'widget': Textarea(attrs={'rows': 10,'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('email', 'user_name', 'full_name', 'password1', 'password2', 'is_active', 'is_staff')
            }
        ),
    )
    
admin.site.register(CustomUserModel, UserAdminConfig)

@admin.register(ClientProfile)
class ClienteProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'profession']
    list_display_links = ['id', 'user', 'profession',]


@admin.register(ProfessionalProfile)
class ProfessionalProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'profession']
    list_display_links = ['id', 'user', 'profession',]


