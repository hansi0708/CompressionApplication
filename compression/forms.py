from django import forms  
from .models import File_Form

class FileForm(forms.ModelForm):  
    class Meta:
        model = File_Form
        fields=['file']
              