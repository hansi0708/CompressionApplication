import datetime
import platform
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pytz
from pdf2image import convert_from_path
import os
from django.shortcuts import render
from CompressionApplication.function import get_size_format
from Conversion.function import excelTOpdf, imageTOpdf, pdfTOexcel, pdfTOtext, pdfTOword, textTOpdf, wordTOpdf
from .forms import FileForm
import pyrebase
from firebase_admin import  storage
import time
from datetime import datetime, timezone
from django.core.files.storage import default_storage
import uuid
from reportlab.lib.pagesizes import letter

#FIREBASE CONFIG
config = {
  'apiKey': "AIzaSyBbNBjeBbpTnaq2ikJ2Aut5UvW0KqhQ7dQ",
  'authDomain': "compression-tool-6af95.firebaseapp.com",
  'databaseURL': "https://compression-tool-6af95-default-rtdb.firebaseio.com",
  'projectId': "compression-tool-6af95",
  'storageBucket': "compression-tool-6af95.appspot.com",
  'messagingSenderId': "295626631784",
  'appId': "1:295626631784:web:ed35e114286e3d3b6069dd",
  'measurementId': "G-2XZEBYKFC6"
}


# Initialising database, auth, firebase and storage   
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage=firebase.storage()


#TEXT TO PDF
def textToPDF(request):
    uploadFile = FileForm()
    return render(request,"TextToPDF.html",{'form':uploadFile}) 

def text2pdf(request):
	
	if request.method == 'POST':  
		uploadFile = FileForm(request.POST, request.FILES) 

		if uploadFile.is_valid(): 
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_text_to_pdf_converted.pdf"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='pdf'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size))

			#TEXT TO PDF CONVERSION
			textTOpdf(uFile.file.path,new_filename)
			
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']
			
			conv_id = uuid.uuid4()
	
			#Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_pdf_to_text_converted.txt"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='txt'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size))
			
			#PDF TO TEXT CONVERSION
			pdfTOtext(uFile.file.path,new_filename)

			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']
			
			conv_id = uuid.uuid4()
			
			#Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_pdf_to_excel_converted.xlsx"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='xlsx'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size))

			#PDF TO EXCEL CONVERSION
			pdfTOexcel(uFile.file.path,new_filename)
			
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)

			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_excel_to_pdf_converted.pdf"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='pdf'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size)) 

			#EXCEL TO PDF CONVERSION
			excelTOpdf(uFile.file.path,new_filename)
			
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/') 
		
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_pdf_to_word_converted.docx"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='docx'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size)) 

			#PDF TO WORD CONVERSION
			pdfTOword(uFile.file.path,new_filename)
						
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
		
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)
			   
            #NEW FILENAME
			new_filename = f"{filename}_word_to_pdf_converted.pdf" 
  
			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='pdf'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1] 

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size))  

			#WORD TO PDF CONVERSION
			wordTOpdf(uFile.file.path,new_filename)
			
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)
			
            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}_jpg_to_pdf_converted.pdf"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='pdf'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]

            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size))

			#JPG TO PDF CONVERSION
			imageTOpdf(uFile.file.path,new_filename)
			
			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(new_filename)
			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
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
			uFile = uploadFile.save(commit=False)
			uFile.file = request.FILES['file']
	
			#FILENAME
			filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
			new_filename = f"{filename}.jpg"

			#FILE TYPE
			file_type = uFile.file.url.split('.')[-1]
			file_type = file_type.lower()

			#NEW FILE TYPE
			new_file_type='jpg'

			#Saving original file locally
			uFile.save()

            #Filename to store in firebase
			if platform.system() == "Windows":
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('\\')[-1] 
			elif platform.system() == "Linux" :
				file_name= uFile.file.url.split('/')[-1]
				new_file_name= new_filename.split('/')[-1]
			
            #Get the original file size in bytes
			file_size = os.path.getsize(uFile.file.path)

            #Print size 
			print("[*] Size :", get_size_format(file_size)) 

			#PDF TO JPG CONVERSION
			# Convert PDF to a list of PIL Image objects
			images = convert_from_path(uFile.file.path, dpi=200)

			idToken=request.session['uid']
			a=authe.get_account_info(idToken)
			a=a['users']
			a=a[0]
			a=a['localId']

			conv_id = uuid.uuid4()

            #Storing original file in firebase storage
			storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).put(uFile.file.path)
			
			# Save each image to the output path
			for i, image in enumerate(images):
				image_path = f"{filename}_{i + 1}.jpg"
				image.save(image_path, "JPEG")
				storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).put(image_path)

			
			tz =pytz.timezone('Asia/Kolkata')
			time_now=datetime.now(timezone.utc).astimezone(tz)
			millis=int(time.mktime(time_now.timetuple()))
			
			org_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).get_url(idToken)
			new_url=storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).get_url(idToken)
			
			data={
                'user_id':a,
                'date_time':millis,
                'file_name':file_name,
                'new_file_name':new_file_name,
                'file':org_url,
			    'file_type':file_type,
			    'file_size':file_size,
			    'new_file':new_url,
			    'new_file_type':new_file_type
		    }

            #Storing data in conversion table in Firebase Realtime Database
			database.child('conversion').child(conv_id).set(data)

            #Deleting from local storage
			default_storage.delete(uFile.file.path)
			default_storage.delete(new_filename)  
			
			return HttpResponseRedirect('/userConvList/')
	
	else:  
		uploadFile = FileForm()  

	return render(request,"PDFtoJPG.html",{'form':uploadFile})				
