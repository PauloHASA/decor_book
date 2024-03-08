from typing import Any
from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import   authenticate
from .models import CustomUserModel, ClientProfile, ProfessionalProfile
from .models import  CompanyProfile, ConstructionProfile, PROFISSION_CHOICES

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
        widget=forms.TextInput(attrs={"placeholder": ""})
    )
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": ""})
    )
    profession = forms.CharField(
        required=True, widget=forms.Select(choices=PROFISSION_CHOICES)
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )       
    
    class Meta:
        model = ClientProfile
        fields = ['email', 'full_name', 'profession', 'password1', 'password2']
        

class ProfessionalForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder":""})
    )
    full_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": ""})
    )
    site = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"placeholder": ""})
    )
    profession = forms.CharField(
        required=True, widget=forms.Select(choices=PROFISSION_CHOICES)
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": ""}), required=True
    )       

    class Meta:
        model = ProfessionalProfile
        fields = ['email', 'full_name','site', 'profession', 'password1', 'password2']