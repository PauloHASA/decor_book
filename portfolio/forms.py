from django import forms 
from .models import NewProject, ImagePortfolio
from django.forms.widgets import ClearableFileInput


class FormStepOne(forms.ModelForm):
    class Meta:
        model = NewProject
        fields = ['name', 'partner', 'summary','data_initial', 'data_final']
        widgets = {
            'data_initial': forms.DateInput(attrs={'type':'date'}),
            'data_final': forms.DateInput(attrs={'type':'date'})
        }

    def clear(self):
        cleaned_data = super().clean()
        data_initial = cleaned_data.get('data_initial')
        data_final = cleaned_data.get('data_initial')
        
        if data_final and data_initial:
            if data_final < data_initial:
                raise forms.ValidationError("A  data final não pode ser maior do que a data inicial.")

class FormStepTwo(forms.ModelForm):
    class Meta:
        model = NewProject
        fields = ['area', 'rooms', 'style', 'categories', 'add_stores']


class FormStepTwoOverwrite(FormStepTwo):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'data_final' in self.fields:
            del self.fields['data_final']


class FormStepThree(forms.ModelForm):       
    class Meta:
        model = ImagePortfolio
        fields = ['img_upload']