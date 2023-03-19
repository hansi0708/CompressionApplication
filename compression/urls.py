from django.urls import path
from . import views
from CompressionApplication import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.imageCompression),
    path('compressImage/', views.compressImage, name = 'create'),
    
    path('compressPPT/',views.compressPPT),
    path('pptCompression/',views.pptCompression),

    path('compressWord/',views.compressWord),
    path('wordCompression/',views.wordCompression),

    path('compressPDF/',views.CompressPDF),
    path('pdfCompression/',views.pdfCompression),

    #path('download/', views.download_file),
   # path('download/', views.download_file, name='download'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    