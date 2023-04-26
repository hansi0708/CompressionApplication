#Import os module
import os
import platform
from PIL import Image
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import FileForm
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import zlib,sys
import pyrebase
from firebase_admin import storage
from compress_pptx.compress_pptx import CompressPptx
import time
from datetime import datetime, timezone
import pytz
from django.core.files.storage import default_storage
import uuid

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
    return render(request,"ImageCompression.html",{'form':uploadFile})
     
def compressImage(request):
            
    if request.method == 'POST':  
        uploadFile = FileForm(request.POST, request.FILES) 

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

            #Image compression code
            quality=90
            
            #Loading image to memory
            img = Image.open(uFile.file.path)

            #Print original image shape
            print("[*] Image shape:", img.size)
            
            #Get the original file size in bytes
            file_size = os.path.getsize(uFile.file.path)

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))

            
            try:
                #Save the image with the corresponding quality and optimize set to True
                img.save(new_filename, quality=quality, optimize=True)

            except OSError:
                #Convert the image to RGB mode first
                img = img.convert("RGB")

                #Save the image with the corresponding quality and optimize set to True
                img.save(new_filename, quality=quality, optimize=True)

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            print(saving_diff)

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "ImageCompression.html", {'form':uploadFile,"msg":message})
            
            else:

                #Print the saving percentage
                print(f"[+] File size change: {saving_diff/file_size*100:.2f}% of the original file size.")
                
                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()
                #Storing files in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                tz =pytz.timezone('Asia/Kolkata')
                time_now=datetime.now(timezone.utc).astimezone(tz)
                millis=int(time.mktime(time_now.timetuple()))

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
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
    
    return render(request,"ImageCompression.html",{'form':uploadFile})


# PPT COMPRESSION
def compressPPT(request):
    uploadFile = FileForm()
    return render(request,"CompressPPT.html",{'form':uploadFile})
	 
def pptCompression(request):

    if request.method == 'POST':
        uploadFile = FileForm(request.POST, request.FILES)

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
            CompressPptx(uFile.file.path,new_filename).run()

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressPPT.html", {'form':uploadFile,"msg":message})
            
            else:
                #Print the saving percentage
                print(f"[+] File size change: {saving_diff/file_size*100:.2f}% of the original file size.")

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']
                
                comp_id = uuid.uuid4()
                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                tz =pytz.timezone('Asia/Kolkata')
                time_now=datetime.now(timezone.utc).astimezone(tz)
                millis=int(time.mktime(time_now.timetuple()))

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
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

    return render(request,"CompressPPT.html",{'form':uploadFile})


# WORD COMPRESSION           
def compressWord(request):
    uploadFile = FileForm()
    return render(request,"CompressWord.html",{'form':uploadFile})
           
def wordCompression(request):

    if request.method == 'POST':  
        uploadFile = FileForm(request.POST, request.FILES) 
        
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
                file_name= uFile.file.url.split('\\')[-1]
                new_file_name= new_filename.split('\\')[-1] 
            elif platform.system() == "Linux" :
                file_name= uFile.file.url.split('/')[-1]
                new_file_name= new_filename.split('/')[-1] 

            #Get the original file size in bytes
            file_size = os.path.getsize(uFile.file.path)

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))    

            #Word compression code
            with open(uFile.file.path, mode="rb") as fin, open(new_filename, mode="wb") as fout:
                data = fin.read()
                compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
                print(f"Original size: {sys.getsizeof(data)}")

                # Original size: 1000033
                print(f"Compressed size: {sys.getsizeof(compressed_data)}")

                # Compressed size: 1024
                fout.write(compressed_data)

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            print(saving_diff)

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressWord.html", {'form':uploadFile,"msg":message})

            else:
                #Print the saving percentage
                print(f"[+] File size change: {saving_diff/file_size*100:.2f}% of the original file size.")

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()

                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                tz =pytz.timezone('Asia/Kolkata')
                time_now=datetime.now(timezone.utc).astimezone(tz)
                millis=int(time.mktime(time_now.timetuple()))

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
            
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
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

    return render(request,"CompressWord.html",{'form':uploadFile})


# PDF COMPRESSION
def CompressPDF(request):
    uploadFile = FileForm()
    return render(request,"CompressPDF.html",{'form':uploadFile})

def pdfCompression(request):

    if request.method == 'POST': 
        uploadFile = FileForm(request.POST, request.FILES)

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
                file_name= uFile.file.url.split('\\')[-1]
                new_file_name= new_filename.split('\\')[-1] 
            elif platform.system() == "Linux" :
                file_name= uFile.file.url.split('/')[-1]
                new_file_name= new_filename.split('/')[-1] 

            #Get the original file size in bytes
            file_size = os.path.getsize(uFile.file.path)

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(file_size))

            #PDF compression code
            PDFNet.Initialize("demo:1679382800894:7d172aad03000000006e4e8c2e43b0a1edd4e0fe31883bada9d6815484")
            doc = PDFDoc(uFile.file.path)

            #Optimize PDF with the default settings
            doc.InitSecurityHandler()

            #Reduce PDF size by removing redundant information and compressing data streams
            Optimizer.Optimize(doc)

            doc.Save(new_filename, SDFDoc.e_linearized)
            doc.Close()

            #Get the new file size in bytes
            new_file_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_file_size))

            #Calculate the saving bytes
            saving_diff = new_file_size - file_size

            if saving_diff >= 0:
                message  = "This file cannot be compressed any further."
                return render(request, "CompressPDF.html", {'form':uploadFile,"msg":message})

            else:
                #Print the saving percentage
                print(f"[+] File size change: {saving_diff/file_size*100:.2f}% of the original file size.")

                idToken=request.session['uid']
                a=authe.get_account_info(idToken)
                a=a['users']
                a=a[0]
                a=a['localId']

                comp_id = uuid.uuid4()

                #Storing original file in firebase storage
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).put(uFile.file.path)
                storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).put(new_filename)

                tz =pytz.timezone('Asia/Kolkata')
                time_now=datetime.now(timezone.utc).astimezone(tz)
                millis=int(time.mktime(time_now.timetuple()))

                org_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).get_url(idToken)
                new_url=storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).get_url(idToken)
                
                data={
                    'user_id':a,
                    'date_time':millis,
                    'file_name':file_name,
                    'new_file_name':new_file_name,
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
    
    return render(request,"CompressPDF.html",{'form':uploadFile})

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"