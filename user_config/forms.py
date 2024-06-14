from typing import Any
from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.forms import FileInput
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import CustomUserModel, ClientProfile, ProfessionalProfile
from .models import  CompanyProfile, ConstructionProfile, PROFISSION_CHOICES
from .controllers import FolderUserPost

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": ""})
    )
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": ""})
    )
    user_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": ""})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )

    class Meta:
        model = CustomUserModel
        fields = (
            "email",
            "full_name",
            "user_name",
            "password1",
            "password2",
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Esta email já está em uso.")
        return email
    
    def clean_user_name(self):
        user_name = self.cleaned_data.get('user_name')
        if CustomUserModel.objects.filter(user_name=user_name).exists():
            raise forms.ValidationError("Esta Usuário já está em uso.")
        return user_name
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("As senhas não coincidem."))
        
        return cleaned_data
        
        
class LoginUserForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"autocomplete":"new-password"}),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"autocomplete":"new-password"}),
    )
    remember_me = forms.BooleanField(
        required=False, initial=True, widget=forms.CheckboxInput
    )
    
    class Meta:
        model = CustomUserModel
        fields = ("email", "password")
        
    def clean(self):
        if self.is_valid():
            email =  self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid credentials")
            

class ClientForm(forms.ModelForm):    
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "janedoe@email.com"})
    )
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Nome completo"})
    )
    profession = forms.ChoiceField(
        required=True, 
        widget=forms.Select(attrs={"placeholder": "Defina sua profissão"}),
        choices=PROFISSION_CHOICES,
        )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )       
    
    class Meta:
        model = ClientProfile
        fields = ['email', 'full_name', 'profession', 'password1', 'password2']
        

class ProfessionalForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "janedoe@email.com"})
    )
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Nome completo"})
    )
    site = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "www.professional.com"})
    )
    profession = forms.ChoiceField(
        required=True, 
        widget=forms.Select(attrs={"placeholder": "Defina sua profissão"}),
        choices=PROFISSION_CHOICES,
        )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )       

    class Meta:
        model = ProfessionalProfile
        fields = ['email', 'full_name','site', 'profession', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ja esta em uso.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas nao correspondem.")
            
        return cleaned_data
        


class CompanyForm(forms.ModelForm):
    
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Nome social"})
    )
    
    fantasy_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Que aparecerá no perfil"})
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "empresa@email.com"})
    )
    
    product = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "Especifique o produto vendido"})
    )
    
    site = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": "www.company.com"})
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "*****************"}), required=True
    )       

    class Meta:
        model = CompanyProfile
        fields = ['fantasy_name', 'product', 'site']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ja esta em uso.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas nao correspondem.")
            
        return cleaned_data
    
    def save(self, commit=True):
        user = CustomUserModel(
            email=self.cleaned_data['email'],
            user_name=self.cleaned_data['email'],
            full_name=self.cleaned_data['full_name'],
            is_company=True,
        )
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
            company_profile = CompanyProfile(
                user=user,
                fantasy_name = self.cleaned_data['fantasy_name'],
                product = self.cleaned_data['product'],
                site = self.cleaned_data['site'],
            )
            company_profile.save()
            
        return user 


class ProfessionalProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(label='Imagem de Perfil', required=False, widget=FileInput(attrs={'id': 'profile-picture-input'}))
    
    class Meta:
        model = ProfessionalProfile
        fields = ['profession', 'site', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfessionalProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def save(self, commit=True):
        professional_profile = super(ProfessionalProfileForm, self).save(commit=False)
        
        if 'profile_picture' in self.cleaned_data:
            image = self.cleaned_data['profile_picture']
            if image:
                professional_profile.profile_picture = image
                if commit:
                    professional_profile.save()
        
        return professional_profile
    
    
class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)
    old_password = forms.CharField(label='Senha Antiga', widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(label='Nova Senha', widget=forms.PasswordInput, required=False)

    profession = forms.ChoiceField(choices=PROFISSION_CHOICES, required=False)
    site = forms.CharField(required=False)

    class Meta:
        model = CustomUserModel
        fields = ['email', 'full_name']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            if hasattr(instance, 'professionalprofile'):
                professional_profile = instance.professionalprofile
                self.fields['profession'].initial = professional_profile.profession
                self.fields['site'].initial = professional_profile.site

    def clean_email(self):
        return self.instance.email

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if old_password and not self.instance.check_password(old_password):
            raise forms.ValidationError("Senha antiga incorreta.")
        return old_password

    def save(self, commit=True):
        user = super(ProfileEditForm, self).save(commit=False)
        if commit:
            new_password = self.cleaned_data.get('new_password')
            if new_password:
                user.password = make_password(new_password)
            user.save()

            if hasattr(self.instance, 'professionalprofile'):
                professional_profile = self.instance.professionalprofile
                professional_profile.profession = self.cleaned_data.get('profession')
                professional_profile.site = self.cleaned_data.get('site')
                if 'profile_picture' in self.cleaned_data:
                    professional_profile.profile_picture = self.cleaned_data['profile_picture']
                professional_profile.save()
            else:
                professional_profile = ProfessionalProfile(
                    user=user,
                    profession=self.cleaned_data.get('profession'),
                    site=self.cleaned_data.get('site')
                )
                if 'profile_picture' in self.cleaned_data:
                    professional_profile.profile_picture = self.cleaned_data['profile_picture']
                professional_profile.save()
        return user