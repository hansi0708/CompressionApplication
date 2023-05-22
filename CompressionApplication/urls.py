from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    
    path('admin/',include('Admin.urls')),
    path('',include('User.urls')),
    path('imageCompression/',include('compression.urls')),
    path('PDFtoJPG/',include('Conversion.urls')),

   ]