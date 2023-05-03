from django.urls import path
from .import views
from CompressionApplication import settings
from django.conf.urls.static import static

urlpatterns = [

    #PDF TO JPG
    path('',views.PDFtoJPG),
    path('pdf2jpg/',views.pdf2jpg), 

    #TEXT TO PDF
    path('textToPDF/',views.textToPDF),
    path('text2pdf/',views.text2pdf),

    #PDF TO TEXT
    path('PDFtoText/',views.PDFtoText),
    path('pdf2text/',views.pdf2text),

    #PDF TO EXCEL
    path('PDFtoExcel/',views.PDFtoExcel),
    path('pdf2excel/',views.pdf2excel),

    #EXCEL TO PDF
    path('ExcelToPDF/',views.ExcelToPDF),
    path('excel2pdf/',views.excel2pdf),

    #PDF TO WORD
    path('PDFtoWord/',views.PDFtoWord),
    path('pdf2word/',views.pdf2word),

    #WORD TO PDF
    path('WordToPDF/',views.WordToPDF),
    path('word2pdf/',views.word2pdf),

    #JPG TO PDF
    path('JPGtoPDF/',views.JPGtoPDF),
    path('jpg2pdf/',views.jpg2pdf),   
    
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    