from django.db import models

class User(models.Model):
    id = models.CharField(max_length=100,blank=False, null=False)
    name = models.CharField(max_length=50,blank=False, null=False)
    email = models.EmailField(max_length=50,blank=False, null=False)
    centre = models.CharField(max_length=50,blank=False, null=False)
    staff = models.CharField(max_length=50,blank=False, null=False)
    designation = models.CharField(max_length=50,blank=False, null=False)
    department = models.CharField(max_length=50,blank=False, null=False)
    employment_type = models.CharField(max_length=50,blank=False, null=False)
    level = models.CharField(max_length=50,blank=False, null=False)
    password = models.CharField(max_length=50,blank=False, null=False)
    Reset_password = models.CharField(max_length=50,blank=False, null=False)