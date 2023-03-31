from django.db import models

class User(models.Model):
    id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    centre = models.CharField(max_length=50)
    staff = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    employment_type = models.CharField(max_length=50)
    level = models.CharField(max_length=50)