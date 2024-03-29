from django.urls import path
from . import views
from CompressionApplication import settings
from django.conf.urls.static import static

urlpatterns = [

    #Image Compression
    path('',views.imageCompression),
    path('compressImage/', views.compressImage),
    
    #PPT Compression
    path('compressPPT/',views.compressPPT),
    path('pptCompression/',views.pptCompression),

    #Word Compression
    path('compressWord/',views.compressWord),
    path('wordCompression/',views.wordCompression),

    #PDF Compression
    path('compressPDF/',views.CompressPDF),
    path('pdfCompression/',views.pdfCompression),

   ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    