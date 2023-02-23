from django.db import models
from django.forms import ModelForm

# Create your models here.

class InputFile(models.Model):
    input_file = models.FileField()

