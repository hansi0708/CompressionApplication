from django.urls import path
from . import views
from CompressionApplication import settings
from django.conf.urls.static import static
urlpatterns = [
    path('textToPDF/',views.textToPDF),
    path('text2pdf/',views.text2pdf),

    path('PDFtoExcel/',views.PDFtoExcel),
    path('pdf2excel/',views.pdf2excel),

    path('ExcelToPDF/',views.ExcelToPDF),
    path('excel2pdf/',views.excel2pdf),

    path('PDFtoWord/',views.PDFtoWord),
    path('pdf2word/',views.pdf2word),

    path('WordToPDF/',views.WordToPDF),
    path('word2pdf/',views.word2pdf),

    path('JPGtoPDF/',views.JPGtoPDF),
    path('jpg2pdf/',views.jpg2pdf),

    path('',views.PDFtoJPG),
    path('pdf2jpg/',views.pdf2jpg),    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    