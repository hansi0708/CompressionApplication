from django import forms  
from django.forms import ModelForm
from .models import InputFile

class File_Form(forms.ModelForm):  
    class Meta:
        model = InputFile
         # for creating file input  
        fields = ['input_file']
