from django.shortcuts import render
import tabula 
import os 
#mport pyautogui
import pdf2docx, docx2pdf
import PyPDF2
from pdf2docx import Converter
#from tabula.io import read_pdf
import tabula 
import pandas as pd
from pdf2image import convert_from_path
import img2pdf
from PIL import Image 
import textwrap
from fpdf import FPDF
import os
#import win32com.client
#from pywintypes import com_error
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
# Create your views here.


def textToPDF(request):
    return render(request,"TextToPDF.html") 

def text2pdf(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			pdf = FPDF()      
			pdf.add_page()  # Add a page 
			pdf.set_font("Arial", size = 15)    # set style and size of font  # that you want in the pdf
			f = open(user_pr.file, 'r')       # open the text file in read mode 
			for x in f:      # insert the texts in pdf 
				pdf.cell(200,10, txt = x, ln = 2, align = 'L') 
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"	
			pdf.output(f"{new_filename}.pdf","wb")    # save the pdf with name .pdf 
			# f.save(new_filename)
			return HttpResponse("Text to PDF converted successfuly")
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"TextToPDF.html",{'form':uploadFile})		


def PDFtoExcel(request):
	return render(request,"PDFtoExcel.html") 

def pdf2excel(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"	
			tabula.convert_into(user_pr.file, f"{new_filename}.csv", pages="all", output_format = "csv", stream = True)
			return HttpResponse("PDF to Excel converted successfuly")
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"PDFtoExcel.html",{'form':uploadFile})				


def ExcelToPDF(request):
	return render(request,"ExcelToPDF.html") 

def excel2pdf(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			WB_PATH = open(user_pr.file, 'rb')   # Path to original excel file
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"	
			PATH_TO_PDF = f"{new_filename}.pdf","wb"    # PDF path when saving
			#excel = win32com.client.Dispatch("Excel.Application")
			# excel.Visible = False
			# try:
			# 	print('Start conversion to PDF')# Open
			# 	wb = excel.Workbooks.Open(WB_PATH)# Specify the sheet you want to save by index. 1 is the first (leftmost) sheet.
			# 	ws_index_list = [1,2,3,4,5,6,7,8,9,10,11,12]
			# 	wb.WorkSheets(ws_index_list).Select()# Save
			# 	wb.ActiveSheet.ExportAsFixedFormat(0, PATH_TO_PDF)
			# except com_error as e:
			# 	print('failed.')
			# else:
			# 	print('Succeeded.')
			# finally:
			# 	wb.Close()
			# 	excel.Quit()
			return HttpResponse("Excel to PDF converted successfuly") 
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"ExcelToPDF.html",{'form':uploadFile})				
		

def PDFtoWord(request):
	return render(request,"PDFtoWord.html") 

def pdf2word(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"	
			cv = Converter(user_pr.file)
			cv.convert(new_filename, start = 0, end = None)
			return HttpResponse("PDF to Word converted successfuly")   # pdf2docx.parse(user_pr.file, f"{new_filename}.docx", start=0, end=None)
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"PDFtoWord.html",{'form':uploadFile})		



def WordToPDF(request):
	return render(request,"WordToPDF.html") 

def word2pdf(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			open_file = open(user_pr.file, 'rb')# docx2pdf.convert(open_file)
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"
			file_save = open(f"{new_filename}.pdf", "w")
			docx2pdf.convert(open_file, file_save)
			return HttpResponse("Word to PDF converted successfuly")
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"WordToPDF.html",{'form':uploadFile})

			
			

def JPGtoPDF(request):
	return render(request,"JPGtoPDF.html") 

def jpg2pdf(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			image = Image.open(user_pr.file)  # opening image\
			pdf_bytes = img2pdf.convert(image.filename)   # converting into chunks using img2pdf
			filename, ext = os.path.splitext(user_pr.file.path)
			new_filename = f"{filename}_converted"
			with open(f"{new_filename}.pdf", "wb") as file:      #write file 
				file.write(pdf_bytes)
			image.close()    # closing image file
			user_pr.file.close()     # closing pdf file
			print("Successfully made pdf file")    # output
			return HttpResponse("JPG to PDF converted successfuly")
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"JPGtoPDF.html",{'form':uploadFile})


def PDFtoJPG(request):
	return render(request,"PDFtoJPG.html") 

def pdf2jpg(request):
	if request.method == 'POST':  
		print("1")
		uploadFile = FileForm(request.POST, request.FILES) 
		print("2") 
		if uploadFile.is_valid():  
			print("3")
			user_pr = uploadFile.save(commit=False)
			print("4")
			user_pr.file = request.FILES['file']
			print("5")
			file_type = user_pr.file.url.split('.')[-1]
			print("6")
			file_type = file_type.lower()
			print("7")
			user_pr.save()
			print("8")
			poppler_path = r"C:\Users\nutan\Downloads\Release-23.01.0-0 (1)\poppler-23.01.0\Library\bin"
			images = convert_from_path(user_pr.file, poppler_path= poppler_path)
			for image in images:
				image.save(f"{images.index(image)}.jpg", "JPEG")
			return HttpResponse("PDF to JPG converted successfuly")
	else:  
		print("else1")
		uploadFile = FileForm()  
		print("else2")
	return render(request,"PDFtoJPG.html",{'form':uploadFile})				
		


