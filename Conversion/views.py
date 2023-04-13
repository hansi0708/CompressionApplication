from django.shortcuts import render
import tabula 
import os 
import pdf2docx, docx2pdf
import PyPDF2
from pdf2docx import Converter
from tabula.io import read_pdf
import tabula 
import pandas as pd
from pdf2image import convert_from_path
import img2pdf
from PIL import Image 
import textwrap
from fpdf import FPDF 
import os
from collections.abc import MutableMapping
# Import mimetypes module
import mimetypes
# import os module
import os
from PIL import Image
# Import HttpResponse module
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import FileForm
from .models import File_Form
import pdftables_api
import  jpype, asposecells  
from pdf2jpg import pdf2jpg
import aspose.words as aw


#TEXT TO PDF
def textToPDF(request):
    
    uploadFile = FileForm()
    return render(request,"TextToPDF.html",{'form':uploadFile}) 

def text2pdf(request):

	if request.method == 'POST':  

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()

			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_text_to_pdf_converted.pdf"
			# load TXT document
			doc = aw.Document(user_pr.file.path)
			# save TXT as PDF file
			doc.save(new_filename, aw.SaveFormat.PDF)
			
			return HttpResponse("Text to PDF converted successfuly")
	
	else:  
		uploadFile = FileForm()  

	return render(request,"TextToPDF.html",{'form':uploadFile})		


#PDF TO TEXT
def PDFtoText(request):
    
    uploadFile = FileForm()
    return render(request,"PDFtoText.html",{'form':uploadFile}) 

def pdf2text(request):

	if request.method == 'POST':  

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()
			
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_pdf_to_text_converted"

			PdfFileObject = open(user_pr.file.path, 'rb')
			output_file = open(f"{new_filename}.txt", "w", encoding="utf-8")
			pdfReader = PyPDF2.PdfReader(PdfFileObject)
			numOfPages = len(pdfReader.pages)

			# print(f"No. of pages: {pdfReader.numPages}")
			for i in range(numOfPages):

				page = pdfReader.pages[i]
				text = page.extract_text()
				output_file.write(text)

			output_file.close()    
			PdfFileObject.close()

			return HttpResponse("PDF to Text converted successfuly")
	
	else:  
		uploadFile = FileForm()  

	return render(request,"PDFtoText.html",{'form':uploadFile})	


#PDF TO EXCEL
def PDFtoExcel(request):

	uploadFile = FileForm()
	return render(request,"PDFtoExcel.html",{'form':uploadFile}) 

def pdf2excel(request):

	if request.method == 'POST': 

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()

			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_pdf_to_excel_converted"	

			c = pdftables_api.Client('am6ebz6z2eei')
			c.xlsx(user_pr.file.path, new_filename)
			
			# tabula.convert_into(user_pr.file.path, f"{new_filename}.csv", pages="all", output_format = "csv", stream = True)
			return HttpResponse("PDF to Excel converted successfuly")
	
	else:  
		uploadFile = FileForm() 

	return render(request,"PDFtoExcel.html",{'form':uploadFile})				


#EXCEL TO PDF
def ExcelToPDF(request):

	uploadFile = FileForm()
	return render(request,"ExcelToPDF.html",{'form':uploadFile}) 

def excel2pdf(request):

	if request.method == 'POST':  

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()
			
			WB_PATH = open(user_pr.file.path, 'rb')   # Path to original excel file
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_excel_to_pdf_converted.pdf"
			import  jpype     
			import  asposecells 
			jpype.startJVM() 
			from asposecells.api import Workbook
			
			workbook = Workbook(user_pr.file.path)
			
			workbook.save(new_filename)
			# jpype.shutdownJVM()
			# Open Microsoft Excel
			# excel = client.DispatchEx("Excel.Application")
			# excel.interactive = False
			# excel.Visible = False
			# # Read Excel File
			# sheets = excel.Workbooks.Open(WB_PATH)
			# work_sheets = sheets.Worksheets[0]
			# new_filename = f"{filename}_Excel_to_pdf_converted"
			# # Convert into PDF File
			# work_sheets.ActiveSheet.ExportAsFixedFormat(0, new_filename)
			# work_sheets.close()
			
			# # PATH_TO_PDF = open(f"{new_filename}.pdf","w+" ) 
			# with open(f"{new_filename}.pdf", "wb") as file:  # PDF path when saving
			# 	file.write()
			# WB_PATH.close()
			# user_pr.file.close()
			
			# excel = win32com.client.Dispatch("Excel.Application")
			# excel.Visible = False
			# try:
			# 	print('Start conversion to PDF')
			# 	# Open
			# 	wb = excel.Workbooks.Open(WB_PATH)
			# 	# Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
			# 	ws_index_list = [1,2,3,4,5,6,7,8,9,10,11,12]
			# 	wb.WorkSheets(ws_index_list).Select()
			# 	# Save
			# 	wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)
			# except com_error as e:
			# 	print('failed.')
			# else:
			# 	print('Succeeded.')
			# finally:
			# 	 
			return HttpResponse("Excel to PDF converted successfuly") 
		
	else:  
		uploadFile = FileForm()  

	return render(request,"ExcelToPDF.html",{'form':uploadFile})				
		

#PDF TO WORD
def PDFtoWord(request):

	uploadFile = FileForm()
	return render(request,"PDFtoWord.html",{'form':uploadFile}) 

def pdf2word(request):

	if request.method == 'POST':  

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()

			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_pdf_to_word_converted.docx"	
			cv = Converter(user_pr.file.path)
			cv.convert(new_filename, start = 0, end = None)

			return HttpResponse("PDF to Word converted successfuly")   # pdf2docx.parse(user_pr.file, f"{new_filename}.docx", start=0, end=None)
	
	else:  
		uploadFile = FileForm()  

	return render(request,"PDFtoWord.html",{'form':uploadFile})		


#WORD TO PDF
def WordToPDF(request):

	uploadFile = FileForm()
	return render(request,"WordToPDF.html",{'form':uploadFile}) 

def word2pdf(request):

	if request.method == 'POST':  

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()
			open_file = open(user_pr.file.path, 'r',encoding='utf-8')# docx2pdf.convert(open_file)
			
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_word_to_pdf_converted.pdf"
			
			doc = aw.Document(user_pr.file.path)
            # Save as PDF
			doc.save(new_filename)

			return HttpResponse("Word to PDF converted successfuly")
	
	else:  
		uploadFile = FileForm()  

	return render(request,"WordToPDF.html",{'form':uploadFile})
			
			
#JPG TO PDF
def JPGtoPDF(request):

	uploadFile = FileForm()
	return render(request,"JPGtoPDF.html",{'form':uploadFile}) 

def jpg2pdf(request):

	if request.method == 'POST': 

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()
			
			
			filename, ext = os.path.splitext(user_pr.file.path)
			
			new_filename = f"{filename}_jpg_to_pdf_converted.pdf"
			pdf  = FPDF()
			pdf.set_auto_page_break(0)

			img_list = [x for x in os.listdir('user_pr.file.path')]

			for img in img_list:
				pdf.add_page()
				image = user_pr.file.path + img
				pdf.image(image,w=200,h=260) 

			pdf.output("images.pdf")
				    
			print("Successfully made pdf file")    # output
			
			return HttpResponse("JPG to PDF converted successfuly")
	
	else:  
		uploadFile = FileForm()  

	return render(request,"JPGtoPDF.html",{'form':uploadFile})


#PDF TO JPG
def PDFtoJPG(request):

	uploadFile = FileForm()
	return render(request,"PDFtoJPG.html",{'form':uploadFile}) 

def pdf2jpg(request):

	if request.method == 'POST':

		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid():  

			user_pr = uploadFile.save(commit=False)
			user_pr.file = request.FILES['file']
			file_type = user_pr.file.url.split('.')[-1]
			file_type = file_type.lower()
			user_pr.save()

			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_pdf_to_jpg_converted"
			poppler_path = r"C:\Users\nutan\Downloads\Release-23.01.0-0 (1)\poppler-23.01.0\Library\bin"
			images = convert_from_path(user_pr.file.path,poppler_path=poppler_path)
			# output = "outfile.jpg"
			for image in range(len(images)):
				# fname = 'image'+str(i)+'.JPG'
				images[image].save('page '+str(image)+'.jpg','JPEG')
				
			return HttpResponse("PDF to JPG converted successfuly")
	
	else:  
		uploadFile = FileForm()  

	return render(request,"PDFtoJPG.html",{'form':uploadFile})				
		


