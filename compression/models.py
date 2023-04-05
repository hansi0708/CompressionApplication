from django.db import models
from django.forms import ModelForm

class File_Form(models.Model):

    file = models.FileField()