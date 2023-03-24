from django import forms  
from django.forms import ModelForm
from .models import File_Form

class FileForm(forms.ModelForm):  
    class Meta:
        model = File_Form
        fields=['file']
              