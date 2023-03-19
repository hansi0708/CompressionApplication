from django.db import models
from django.forms import ModelForm

# Create your models here.

class File_Form(models.Model):
    file = models.FileField()

