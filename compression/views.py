#Import os module
import os
from PIL import Image
#Import HttpResponse module
from django.http.response import HttpResponse
from django.shortcuts import render
from .forms import FileForm
from .models import File_Form
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import zipfile
import io
import zlib,sys
import pyrebase

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


def upload(request):
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
          # handle_uploaded_file(request.FILES['file'])  
           return HttpResponse("File uploaded successfuly")
    else:  
        print("else1")
        uploadFile = FileForm()  
        print("else2")
    return render(request,"ImageCompression.html",{'form':uploadFile}) 
 

def write_data_to_files(inp_data, file_name):
    """
     function : create a csv file with the data passed to this code
     args : inp_data : data to be written to the target file
     file_name : target file name to store the data
     return : none
     assumption : File to be created and this code are in same directory. 
    """
    print(f" *** Writing the data to - {file_name}")
    throwaway_storage = io.StringIO(inp_data)
    with open(file_name, 'w') as f:
        for line in throwaway_storage:
            f.write(line)

def file_compress(inp_file_names, out_zip_file):
    """
    function : file_compress
    args : inp_file_names : list of filenames to be zipped
    out_zip_file : output zip file
    return : none
    assumption : Input file paths and this code is in same directory.
    """
# Select the compression mode ZIP_DEFLATED for compression
# or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED
    print(f" *** Input File name passed for zipping - {inp_file_names}")

# create the zip file first parameter path/name, second mode
    print(f' *** out_zip_file is - {out_zip_file}')
    zf = zipfile.ZipFile(out_zip_file, mode="w")
    try:
        for file_to_write in inp_file_names:
# Add file to the zip file
# first parameter file to zip, second filename in zip
            print(f' *** Processing file {file_to_write}')
            zf.write(file_to_write, file_to_write, compress_type=compression)
    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')
    finally:
# Don't forget to close the file!
        zf.close()


# IMAGE COMPRESSION
def imageCompression(request):
    # idToken=request.session['uid']
    # if idToken!= None:
    #     return render(request,"Login.html")
    # else:
        uploadFile = FileForm()
        return render(request,"ImageCompression.html",{'form':uploadFile})
     
def compressImage(request):
            
    if request.method == 'POST':  

        uploadFile = FileForm(request.POST, request.FILES) 

        if uploadFile.is_valid():

            user_pr = uploadFile.save(commit=False)
            user_pr.file = request.FILES['file']

            #FILE TYPE
            file_type = user_pr.file.url.split('.')[-1]
            file_type = file_type.lower()

            print("url ",user_pr.file.url)
            print("path ",user_pr.file.path)

            new_size_ratio=0.9 
            quality=90
            width=None
            height=None

            #FILENAME
            filename, ext = os.path.splitext(user_pr.file.path)
            print(filename)

            #NEW FILENAME
            new_filename = f"{filename}_compressed{ext}"

            #Saving original file locally
            user_pr.save()

            #Filename to store in firebase
            file_name= user_pr.file.url.split('/')[-1]
            print(file_name)

            #Loading image to memory
            img = Image.open(user_pr.file.path)
            print("file open")

            #Print original image shape
            print("[*] Image shape:", img.size)
            
            #Get the original image size in bytes
            image_size = os.path.getsize(user_pr.file.path)

            #Print size before compression/resizing
            print("[*] Size before compression:", get_size_format(image_size))

            if new_size_ratio < 1.0:
                
                #If resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
                img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
                
                #Print new image shape
                print("[+] New Image shape:", img.size)

            elif width and height:
                
                #If width and height are set, resize with them instead
                img = img.resize((width, height), Image.ANTIALIAS)

                #Print new image shape
                print("[+] New Image shape:", img.size)
            
            try:
              
                #Save the image with the corresponding quality and optimize set to True
                img.save(new_filename, quality=quality, optimize=True)

            except OSError:
              
                #Convert the image to RGB mode first
                img = img.convert("RGB")

                #Save the image with the corresponding quality and optimize set to True
                img.save(new_filename, quality=quality, optimize=True)

            print("[+] New file saved:", new_filename)

            #Get the new image size in bytes
            new_image_size = os.path.getsize(new_filename)
            
            #Print the new size in a good format
            print("[+] Size after compression:", get_size_format(new_image_size))

            #Calculate the saving bytes
            saving_diff = new_image_size - image_size

            #Print the saving percentage
            print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")

            data={
			'file':user_pr.file.url,
			'file_type':file_type,
			'image_size':image_size,
			'new_file':new_filename,
			'new_image_size':new_image_size
		    }

            #Storing original file in firebase storage
            storage.child("/comp_files/"+file_name).put(user_pr.file.path)
            print("stored ")

            #org_url=storage.child("/comp_files/"+file_name).get_url(.id)
            #print(org_url)
            
            #Storing data in compression table in Firebase Realtime Database
            database.child('compression').set(user_pr.id)
            database.child('compression').child(user_pr.id).set(data)
            print("Success")  
            print(user_pr.id)  

            return HttpResponse("Image compressed successfuly")  
             
    else:  

        uploadFile = FileForm()
        return render(request,"ImageCompression.html",{'form':uploadFile})

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

# PPT COMPRESSION
def compressPPT(request):
    # idToken=request.session['uid']
    # if idToken!= None:
    #     return render(request,"Login.html")
    # else:
        uploadFile = FileForm()
        return render(request,"CompressPPT.html",{'form':uploadFile})
	 
def pptCompression(request):

    if request.method == 'POST':

        uploadFile = FileForm(request.POST, request.FILES)

        if uploadFile.is_valid():
           
           user_pr = uploadFile.save(commit=False)
           user_pr.file = request.FILES['file']
           file_type = user_pr.file.url.split('.')[-1]
           file_type = file_type.lower()
           user_pr.save()

           filename, ext = os.path.splitext(user_pr.file.path)
           new_filename = f"{filename}_compressed{ext}"

           with open(user_pr.file.path, mode="rb") as fin, open(new_filename, mode="wb") as fout:
            
            data = fin.read()
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            print(f"Original size: {sys.getsizeof(data)}")

            # Original size: 1000033
            print(f"Compressed size: {sys.getsizeof(compressed_data)}")
            
            # Compressed size: 1024
            fout.write(compressed_data)

           with open(new_filename, mode="rb") as fin:
            
            data = fin.read()
            compressed_data = zlib.decompress(data)
            print(f"Compressed size: {sys.getsizeof(data)}")
            
            # Compressed size: 1024
            print(f"Decompressed size: {sys.getsizeof(compressed_data)}")

            return HttpResponse("PPT files compressed successfuly")
    
    else:  

        uploadFile = FileForm()  

    return render(request,"CompressPPT.html",{'form':uploadFile})

# WORD COMPRESSION           
def compressWord(request):
    # idToken=request.session['uid']
    # if idToken!= None:
    #     return render(request,"Login.html")
    # else:
        uploadFile = FileForm()
        return render(request,"CompressWord.html",{'form':uploadFile})
           
def wordCompression(request):

    if request.method == 'POST':  
        
        uploadFile = FileForm(request.POST, request.FILES) 
        
        if uploadFile.is_valid(): 
           
           user_pr = uploadFile.save(commit=False)
           user_pr.file = request.FILES['file']
           file_type = user_pr.file.url.split('.')[-1]
           file_type = file_type.lower()
           user_pr.save()

           filename, ext = os.path.splitext(user_pr.file.path)
           new_filename = f"{filename}_compressed{ext}"

           with open(user_pr.file.path, mode="rb") as fin, open(new_filename, mode="wb") as fout:
            
            data = fin.read()
            compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
            print(f"Original size: {sys.getsizeof(data)}")

            # Original size: 1000033
            print(f"Compressed size: {sys.getsizeof(compressed_data)}")

            # Compressed size: 1024
            fout.write(compressed_data)

           with open(new_filename, mode="rb") as fin:

            data = fin.read()
            compressed_data = zlib.decompress(data)
            print(f"Compressed size: {sys.getsizeof(data)}")

            # Compressed size: 1024
            print(f"Decompressed size: {sys.getsizeof(compressed_data)}")

           return HttpResponse("WORD file compressed successfuly")
        
    else:  

        uploadFile = FileForm()  

    return render(request,"CompressWord.html",{'form':uploadFile})

# PDF COMPRESSION
def CompressPDF(request):
    # idToken=request.session['uid']
    # if idToken!= None:
    #     return render(request,"Login.html")
    # else:
        uploadFile = FileForm()
        return render(request,"CompressPDF.html",{'form':uploadFile})

def pdfCompression(request):

    if request.method == 'POST': 

        uploadFile = FileForm(request.POST, request.FILES)

        if uploadFile.is_valid():  

            user_pr = uploadFile.save(commit=False)
            user_pr.file = request.FILES['file']
            file_type = user_pr.file.url.split('.')[-1]
            file_type = file_type.lower()
            user_pr.save()

            PDFNet.Initialize("demo:1679382800894:7d172aad03000000006e4e8c2e43b0a1edd4e0fe31883bada9d6815484")
            doc = PDFDoc(user_pr.file.path)

            #Optimize PDF with the default settings
            doc.InitSecurityHandler()

            #Reduce PDF size by removing redundant information and compressing data streams
            Optimizer.Optimize(doc)

            filename, ext = os.path.splitext(user_pr.file.path)
            new_filename = f"{filename}_compressed.pdf"
            doc.Save(new_filename, SDFDoc.e_linearized)
            doc.Close()

            return HttpResponse("PDF files compressed successfuly")
        
    else:
          
        uploadFile = FileForm()  

    return render(request,"CompressPDF.html",{'form':uploadFile})

def set_page_size(page_setup, width, height):

    page_setup.page_width = width
    page_setup.page_height = height