from django.urls import path
from . import views
from CompressionApplication import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.profile, name = 'create'),
    #path('download/', views.download_file),
    path('download/', views.download_file, name='download'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    