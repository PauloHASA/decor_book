from django import forms 
from multiupload.fields import MultiFileField

from .models import NewProject, ImagePortfolio


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

class FormStepThree(forms.ModelForm):
    images = MultiFileField(min_num=1, max_num=50)
    
    class Meta:
        model = ImagePortfolio
        fields = ['img_upload']