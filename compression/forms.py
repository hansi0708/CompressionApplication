from django import forms
  
from .models import File_Form

from django.core.exceptions import ValidationError

def validate_file_extension(value, function):
    import os

    ext = os.path.splitext(value.name)[1]  # Get the file extension

    if function == 'imageCompression':
        valid_extensions = ['.jpg', '.png']  # Specify valid file extensions for function1
    elif function == 'compressPDF':
        valid_extensions = ['.pdf']  # Specify valid file extensions for function2
    elif function == 'compressPPT':
        valid_extensions = ['.ppt', '.pptx']
    elif function == 'compressWord':
        valid_extensions = ['.doc', '.docx']
    else:
        valid_extensions = []  # Default: No valid extensions

    if ext.lower() not in valid_extensions:
        raise ValidationError("Invalid file format.")

class FileForm(forms.ModelForm):  
    class Meta:
        model = File_Form
        fields=['file']

    def set_function_context(self, function):
        self.fields['file'].validators = [lambda value: validate_file_extension(value, function)]
              