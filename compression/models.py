from django.db import models
from django.forms import ModelForm

# Create your models here.

class File_Form(models.Model):
    # comp_id=models.AutoField(primary_key=True)
    # comp_id = models.CharField(max_length=100)
    file = models.FileField()
    # file_type = models.CharField(default=None,max_length=50)
    # new_file = models.FileField()
    # image_size = models.CharField(default=None,max_length=50)
    # new_image_size = models.CharField(default=None,max_length=50)
    # time = models.TimeField((""), auto_now=False, auto_now_add=False)
    

