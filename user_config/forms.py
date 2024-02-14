from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import   authenticate
from .models import CustomUserModel

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