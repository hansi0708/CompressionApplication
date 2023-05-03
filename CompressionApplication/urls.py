from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    
    
    path('',include('User.urls')),
    path('imageCompression/',include('compression.urls')),
    path('PDFtoJPG/',include('Conversion.urls')),

   ]