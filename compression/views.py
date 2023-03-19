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
import aspose.words as aw

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
 

# IMAGE COMPRESSION
def imageCompression(request):
    uploadFile = FileForm()
    return render(request,"ImageCompression.html",{'form':uploadFile})
     
def compressImage(request):
            
    if request.method == 'POST':  
        print("1")
        uploadFile = FileForm(request.POST, request.FILES) 
        print("2") 
        print(request)
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
           
           new_size_ratio=0.9 
           quality=90
           width=None
           height=None
           to_jpg=True
 # handle_uploaded_file(request.FILES['file'])  
           #return HttpResponse("File uploaded successfuly")

           # load the image to memory
           img = Image.open(user_pr.file.path)
           # print the original image shape
           print("[*] Image shape:", img.size)
           # get the original image size in bytes
           image_size = os.path.getsize(user_pr.file.path)
            # print the size before compression/resizing
           print("[*] Size before compression:", get_size_format(image_size))
           if new_size_ratio < 1.0:
              # if resizing ratio is below 1.0, then multiply width & height with this ratio to reduce image size
            img = img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
              # print new image shape
            print("[+] New Image shape:", img.size)
           elif width and height:
              # if width and height are set, resize with them instead
            img = img.resize((width, height), Image.ANTIALIAS)
              # print new image shape
            print("[+] New Image shape:", img.size)
            # split the filename and extension
           filename, ext = os.path.splitext(user_pr.file.path)
            # make new filename appending _compressed to the original file name
           if to_jpg:
              # change the extension to JPEG
              new_filename = f"{filename}_compressed.jpg"
           else:
              # retain the same extension of the original image
              new_filename = f"{filename}_compressed{ext}"
           try:
              # save the image with the corresponding quality and optimize set to True
              img.save(new_filename, quality=quality, optimize=True)
           except OSError:
              # convert the image to RGB mode first
              img = img.convert("RGB")
              # save the image with the corresponding quality and optimize set to True
              img.save(new_filename, quality=quality, optimize=True)
           print("[+] New file saved:", new_filename)
            # get the new image size in bytes
           new_image_size = os.path.getsize(new_filename)
            # print the new size in a good format
           print("[+] Size after compression:", get_size_format(new_image_size))
            # calculate the saving bytes
           saving_diff = new_image_size - image_size
            # print the saving percentage
           print(f"[+] Image size change: {saving_diff/image_size*100:.2f}% of the original image size.")
           return HttpResponse("Image compressed successfuly")
            #context=user_pr.objects.all()
        #    return render(request, 'file.html', {'new_filename': new_filename})
    #else:  
    print("else1")
    uploadFile = FileForm()  
    print("else2")
    return render(request,"ImageCompression.html",{'form':uploadFile})
    # context = {"form": form,}
    # return render(request, 'ImageCompression.html', context)

def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

# PPT COMPRESSION
def compressPPT(request):
	return render(request,"CompressPPT.html") 

def pptCompression(request):
    if request.method == 'POST':  
        print("1")
        uploadFile = FileForm(request.POST, request.FILES) 
        print("2") 
        print(request)
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


# WORD COMPRESSION           
def compressWord(request):
	return render(request,"CompressWord.html") 
       
def wordCompression(request):
    if request.method == 'POST':  
        print("1")
        uploadFile = FileForm(request.POST, request.FILES) 
        print("2") 
        print(request)
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
           print(user_pr.file.path)
        #    print(user_pr.file.path)
           doc = aw.Document(user_pr.file.path)
           doc.cleanup()

           shapes = [node.as_shape() for node in doc.get_child_nodes(aw.NodeType.SHAPE, True)]
           for shape in shapes:
                if shape.isImage:
                # It's up to developer to choose the library for image compression.
                    image = Image.open(shape.image_data.to_stream())

        # ...
                # Compress image and set it back to the shape.
                    shape.image_data.set_image("yourCompressedImage")      

           save_options = aw.saving.OoxmlSaveOptions
           save_options.compression_level = aw.saving.CompressionLevel.MAXIMUM

           doc.save("Output.docx", save_options)
           return HttpResponse("WORD file compressed successfuly")
    else:  
        print("else1")
        uploadFile = FileForm()  
        print("else2")
    return render(request,"CompressWord.html",{'form':uploadFile})

# PDF COMPRESSION
def CompressPDF(request):
    idToken=request.session['uid']
    if idToken!= None:
        return render(request,"Login.html")
    else:
        return render(request,"CompressPDF.html")

def pdfCompression(request):
    if request.method == 'POST':  
        print("1")
        uploadFile = FileForm(request.POST, request.FILES) 
        print("2") 
        print(request)
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


            renderer = aw.pdf2word.fixedformats.PdfFixedRenderer()
            pdf_read_options = aw.pdf2word.fixedformats.PdfFixedOptions()
            pdf_read_options.image_format = aw.pdf2word.fixedformats.FixedImageFormat.JPEG
            pdf_read_options.jpeg_quality = 50

            with open ("Input.pdf", 'rb') as pdf_stream:
                pages_stream = renderer.save_pdf_as_images(pdf_stream, pdf_read_options)

            builder = aw.DocumentBuilder()
            for i in range(0, len(pages_stream)):
                # Set maximum page size to avoid the current page image scaling.
                max_page_dimension = 1584
                page_setup = builder.page_setup
                set_page_size(page_setup, max_page_dimension, max_page_dimension)

                page_image = builder.insert_image(pages_stream[i])

                set_page_size(page_setup, page_image.width, page_image.height)
                page_setup.top_margin = 0
                page_setup.left_margin = 0
                page_setup.bottom_margin = 0
                page_setup.right_margin = 0

                if i != len(pages_stream) - 1:
                    builder.insert_break(aw.BreakType.SECTION_BREAK_NEW_PAGE)

            save_options = aw.saving.PdfSaveOptions()
            save_options.cache_background_graphics = True

            builder.document.save("Output.pdf", save_options)
            return HttpResponse("PDF files compressed successfuly")
    else:  
        print("else1")
        uploadFile = FileForm()  
        print("else2")
    return render(request,"CompressPDF.html",{'form':uploadFile})

def set_page_size(page_setup, width, height):

    page_setup.page_width = width
    page_setup.page_height = height


# def upload(request):
#     form = File_Form()
#     if request.method == 'POST':
#         form = File_Form(request.POST, request.FILES)
#         if form.is_valid():
#             user_pr = form.save(commit=False)
#             user_pr.file = request.FILES['file']
#             file_type = user_pr.file.url.split('.')[-1]
#             file_type = file_type.lower()
#             user_pr.save()

# def download_file(request,filename):
#   # Define Django project base directory
#   BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#   # Define text file name
#   #filename = request.FILES['input_file']
#   if filename != '':      
#     # Define the full file path
#     filepath = BASE_DIR  + filename
#     # Open the file for reading content
#     path = open(filepath, 'r')
#     # Set the mime type
#     mime_type, _ = mimetypes.guess_type(filepath)
#     # Set the return value of the HttpResponse
#     response = HttpResponse(path, content_type=mime_type)
#     # Set the HTTP header for sending to browser
    
#     response['Content-Disposition'] = "attachment; filename=%s" % filename
#     # Return the response value
#     #return response
#     return response(filename, as_attachment=True)

#   else: 
#     return render(request, 'file.html')
