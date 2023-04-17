from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),

    #path('', views.welcome),
    path('',include('User.urls')),
    path('imageCompression/',include('compression.urls')),
    #path(r'^imageCompression/',include('compression.urls')),
   # r'^polls/'
    path('PDFtoJPG/',include('Conversion.urls')),
    # path('home/',views.home),

   ]