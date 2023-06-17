import os
import platform
from django.http import HttpResponseRedirect
from django.shortcuts import render
from CompressionApplication.function import get_size_format
from compression.function import  compress_image, compress_pdf, compress_ppt, compress_word
from .forms import FileForm
import pyrebase
from firebase_admin import storage
from datetime import datetime
from django.core.files.storage import default_storage
import uuid
from django.contrib import messages


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


#Initialising database, auth, firebase and storage   
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage=firebase.storage()


# IMAGE COMPRESSION
def imageCompression(request):
    uploadFile = FileForm()
    uploadFile.set_function_context('imageCompression')
    return render(request,"ImageCompression.html",{'form':uploadFile})
     
def compressImage(request):
            
    if request.method == 'POST':  
        uploadFile = FileForm(request.POST, request.FILES) 
        uploadFile.set_function_context('imageCompression')

        if uploadFile.is_valid():
            uFile = uploadFile.save(commit=False)
            uFile.file = request.FILES['file']

            #FILE TYPE
            file_type = uFile.file.url.split('.')[-1]
            file_type = file_type.lower()
            
            #FILENAME
            filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
            new_filename = f"{filename}_compressed{ext}"

            #Saving original file locally
            uFile.save()

            #Filename to store in firebase
            if platform.system() == "Windows":
                file_name= uFile.file.url.split('/')[-1]
                new_file_name= new_filename.split('\\')[-1] 
            elif platform.system() == "Linux" :
                file_name= uFile.file.url.split('/')[-1]
                new_file_name= new_filename.split('/')[-1]

            # Get the original file size in bytes
            file_size = os.path.getsize(uFile.file.path)

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))
            
            #IMAGE COMPRESSION
            compress_image(uFile.file.path,new_filename)

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            print(saving_diff)

            comp_per=-(saving_diff/file_size*100)
            perc=round(comp_per,2)

            #Print the saving percentage
            print(f"[+] File size change: {comp_per:.2f}% of the original file size.")

            if saving_diff >= 0:

                #Deleting from local storage
                default_storage.delete(uFile.file.path)
                default_storage.delete(new_filename)

                data = dict()
                messages.error(request, "Error: This file cannot be compressed any further.")
                return render(request, "ImageCompression.html", {'form':uploadFile})
            
            else:                
                
                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()
                #Storing files in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                now = datetime.now()
                print(now)
                millis= now.strftime('%Y-%m-%d %H:%M:%S')

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
                    'comp_per':perc,
                    'file':org_url,
                    'file_type':file_type,
                    'file_size':file_size,
                    'new_file':new_url,
                    'new_file_size':new_file_size
                }
                
                #Storing data in compression table in Firebase Realtime Database
                database.child('compression').child(comp_id).set(data)  

                #Deleting from local storage
                default_storage.delete(uFile.file.path)
                default_storage.delete(new_filename)

                return HttpResponseRedirect('/userCompList/')  
             
    else:  
        uploadFile = FileForm()
        uploadFile.set_function_context('imageCompression')
    
    return render(request,"ImageCompression.html",{'form':uploadFile})


# PPT COMPRESSION
def compressPPT(request):
    uploadFile = FileForm()
    uploadFile.set_function_context('compressPPT')
    return render(request,"CompressPPT.html",{'form':uploadFile})
	 
def pptCompression(request):

    if request.method == 'POST':
        uploadFile = FileForm(request.POST, request.FILES)
        uploadFile.set_function_context('compressPPT')

        if uploadFile.is_valid():
            uFile = uploadFile.save(commit=False)
            uFile.file = request.FILES['file']

            #FILE TYPE
            file_type = uFile.file.url.split('.')[-1]
            file_type = file_type.lower()
            
            #FILENAME
            filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
            new_filename = f"{filename}_compressed{ext}"

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

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))

            #PPT compression code
            compress_ppt(uFile.file.path,new_filename)

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            comp_per=-(saving_diff/file_size*100)
            perc=round(comp_per,2)
            print(perc)

            #Print the saving percentage
            print(f"[+] File size change: {comp_per:.2f}% of the original file size.")

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressPPT.html", {'form':uploadFile,"msg":message})
            
            else:

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']
                
                comp_id = uuid.uuid4()
                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                now = datetime.now()
                millis= now.strftime('%Y-%m-%d %H:%M:%S')

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
                    'comp_per':perc,
                    'file':org_url,
                    'file_type':file_type,
                    'file_size':file_size,
                    'new_file':new_url,
                    'new_file_size':new_file_size
                }

                #Storing data in compression table in Firebase Realtime Database
                database.child('compression').child(comp_id).set(data)

                #Deleting from local storage
                default_storage.delete(uFile.file.path)
                default_storage.delete(new_filename)
                
                return HttpResponseRedirect('/userCompList/') 
    
    else:  
        uploadFile = FileForm()  
        uploadFile.set_function_context('compressPPT')

    return render(request,"CompressPPT.html",{'form':uploadFile})


# WORD COMPRESSION           
def compressWord(request):
    uploadFile = FileForm()
    uploadFile.set_function_context('compressWord')
    return render(request,"CompressWord.html",{'form':uploadFile})
           
def wordCompression(request):

    if request.method == 'POST':  
        uploadFile = FileForm(request.POST, request.FILES) 
        uploadFile.set_function_context('compressWord')
        
        if uploadFile.is_valid():
            uFile = uploadFile.save(commit=False)
            uFile.file = request.FILES['file']

            #FILE TYPE
            file_type = uFile.file.url.split('.')[-1]
            file_type = file_type.lower()
            
            #FILENAME
            filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
            new_filename = f"{filename}_compressed{ext}"

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

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))    

            #Word compression code
            compress_word(uFile.file.path,new_filename)
            
            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            comp_per=-(saving_diff/file_size*100)
            ccc=round(comp_per,2)

            #Print the saving percentage
            print(f"[+] File size change: {comp_per:.2f}% of the original file size.")

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressWord.html", {'form':uploadFile,"msg":message})

            else:

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()

                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                now = datetime.now()
                millis= now.strftime('%Y-%m-%d %H:%M:%S')

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
                    'comp_per':ccc,
                    'file':org_url,
                    'file_type':file_type,
                    'file_size':file_size,
                    'new_file':new_url,
                    'new_file_size':new_file_size
                }

                #Storing data in compression table in Firebase Realtime Database
                database.child('compression').child(comp_id).set(data)  

                #Deleting from local storage
                default_storage.delete(uFile.file.path)
                default_storage.delete(new_filename)

                return HttpResponseRedirect('/userCompList/') 
        
    else:  
        uploadFile = FileForm() 
        uploadFile.set_function_context('compressWord') 

    return render(request,"CompressWord.html",{'form':uploadFile})


# PDF COMPRESSION
def CompressPDF(request):
    uploadFile = FileForm()
    uploadFile.set_function_context('compressPDF')
    return render(request,"CompressPDF.html",{'form':uploadFile})

def pdfCompression(request):

    if request.method == 'POST': 
        uploadFile = FileForm(request.POST, request.FILES)
        uploadFile.set_function_context('compressPDF')

        if uploadFile.is_valid():  
            print("sfsfd")
            uFile = uploadFile.save(commit=False)
            uFile.file = request.FILES['file']

            #FILE TYPE
            file_type = uFile.file.url.split('.')[-1]
            file_type = file_type.lower()
            
            #FILENAME
            filename, ext = os.path.splitext(uFile.file.path)

            #NEW FILENAME
            new_filename = f"{filename}_compressed{ext}"

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

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))

            #PDF COMPRESSION
            compress_pdf(uFile.file.path,new_filename)

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            comp_per=-(saving_diff/file_size*100)
            print(comp_per)
            ccc=round(comp_per,2)
            print(ccc)

            #Print the saving percentage
            print(f"[+] File size change: {comp_per:.2f}% of the original file size.")

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressPDF.html", {'form':uploadFile,"msg":message})

            else:

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()

                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                now = datetime.now()
                millis= now.strftime('%Y-%m-%d %H:%M:%S')

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
                
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
                    'comp_per':ccc,
                    'file':org_url,
                    'file_type':file_type,
                    'file_size':file_size,
                    'new_file':new_url,
                    'new_file_size':new_file_size
                }

                #Storing data in compression table in Firebase Realtime Database
                database.child('compression').child(comp_id).set(data)

                #Deleting from local storage
                default_storage.delete(uFile.file.path)
                default_storage.delete(new_filename)  

                return HttpResponseRedirect('/userCompList/') 
        
    else:
        uploadFile = FileForm()  
        uploadFile.set_function_context('compressPDF')
    
    return render(request,"CompressPDF.html",{'form':uploadFile})
