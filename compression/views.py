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
from PDFNetPython3.PDFNetPython import PDFDoc, Optimizer, SDFDoc, PDFNet
import zipfile
import zipfile
import io
import pandas as pd
import argparse
import inspect
import os
import tempfile
import zipfile
from fnmatch import fnmatch
from functools import partial
from glob import glob
import yaml
from PIL import Image
import zlib,sys

#from pptx_downsizer.utils import zip_directory, convert_str_to_int

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
        #return render(request,"ImageCompression.html")
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
           print("url ",user_pr.file.url)
           print("path ",user_pr.file.path)
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
    # idToken=request.session['uid']
    # if idToken!= None:
    #     return render(request,"Login.html")
    # else:
        uploadFile = FileForm()
        return render(request,"CompressPPT.html",{'form':uploadFile})
	 
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
        print("else1")
        uploadFile = FileForm()  
        print("else2")
    return render(request,"CompressPPT.html",{'form':uploadFile})


# def downsize_pptx_images(
#     filename,
#     # Image selection:
#     fname_filter=None,  # Only filter files matching this filter (str or callable or None) - or maybe OR filter?
#     fsize_filter=int(0.5*2**20),  # Only convert/reduce files above this filesize (number or None)
#     # Image conversion/save:
#     convert_to="png",
#     img_max_size=2048,
#     quality=90,
#     optimize=True,
#     img_mode=None,
#     fill_color=None,  # e.g. '#ffffff',
#     # Output pptx file:
#     outputfn_fmt="{fnroot}.downsized.pptx",  # "{filename}.downsized.pptx",
#     compress_type=zipfile.ZIP_DEFLATED,
#     wait_before_zip=False,
#     overwrite=None,
#     # Program behavior:
#     on_error='raise',
#     verbose=2,
#     # **writer_kwargs
# ):
#     """Downsize a PowerPoint / OfficeOpen pptx file by compressing the images in the presentation.
#     Args:
#         filename: Filename of the pptx input file.
#         fname_filter: Convert images matching this filename glob pattern, e.g. "*.TIFF".
#         fsize_filter: Convert images with file size larger than this limit in bytes.
#         convert_to: Convert images to this image format - e.g. 'png' or 'jpeg'.
#         img_max_size: If an image is larger than this limit (width or height, in pixels),
#             downscale/reduce the image to this size.
#         quality: Save images with this quality parameter (JPEG only).
#         optimize: Attempt to optimize the image output (for `PIL.Image.save`)
#         img_mode: Convert images to this mode before saving - e.g. 'RGB'.
#         fill_color: If converting images with alpha channels, use this color as background/fill color.
#         outputfn_fmt: The filename format of the generated/downsized pptx file.
#         wait_before_zip: If True, prompt the user to press enter before zipping the files in the temporary directory.
#         compress_type: Use this zip compression method when making the pptx zip file.
#         overwrite: Whether to silently overwrite existing output file if it already exists.
#         verbose: Verbosity level, i.e. how much information to print during execution.
#         on_error: What to do if the program encounters any error.
#             'continue' -> Print error message, then continue.
#             'raise'    -> Abort executing and raise error message.
#     Returns:
#         Filename of the newly generated/downsized pptx file.
#     """
#     # TODO: If output is .jpg, you may need to add one of the following lines to presentation.xlm:
#     #       <Default Extension="jpeg" ContentType="image/jpeg"/>
#     #       <Default Extension="jpg" ContentType="application/octet-stream"/>

#     # OBS: File endings should be \r\n, even on Mac - because MS software.
#     assert os.path.isfile(filename)
#     old_fsize = os.path.getsize(filename)
#     pptx_fnroot, pptx_ext = os.path.splitext(filename)
#     print("\nDownsizing PowerPoint presentation %r (%0.01f MB)...\n" % (filename, old_fsize/2**20))
#     convert_to = convert_to.lower().strip(".")
#     if convert_to == "jpg":
#         print("WARNING: Selected format 'jpg' should be 'jpeg' instead, switching...")
#         convert_to = "jpeg"
#     if img_mode is None and convert_to == 'jpeg':
#         img_mode = 'RGB'
#     filter_desc = []
#     if fsize_filter:
#         filter_desc.append("above %0.01f kB" % (fsize_filter/2**10,))
#     if img_max_size:
#         filter_desc.append("larger than %s pixels" % img_max_size)
#     if fname_filter:
#         filter_desc.append("with filename matching %r" % fname_filter)

#     print(" - Converting image files", " or ".join(filter_desc))
#     if isinstance(fname_filter, str):
#         fname_filter = partial(fnmatch, pat=fname_filter)

#     def ffilter(fname):
#         """Return True if file should be included."""
#         return (
#             (fsize_filter and os.path.getsize(fname) > fsize_filter)
#             and (fname_filter is None or fname_filter(fname))
#         )

#     output_ext = "." + convert_to.strip(".")
#     changed_fns = []
#     new_zip_fn = outputfn_fmt.format(filename=filename, fnroot=pptx_fnroot)
#     with tempfile.TemporaryDirectory() as tmpdirname:
#         pptdir = os.path.join(tmpdirname, "ppt")
#         mediadir = os.path.join(pptdir, "media")
#         if verbose and verbose > 0:
#             print("\nExtracting %r to temporary directory %r..." % (filename, tmpdirname))
#         with zipfile.ZipFile(filename, 'r') as zipfd:
#             zipfd.extractall(tmpdirname)
#         if verbose and verbose > 1:
#             print("pptdir:", pptdir)
#             print("mediadir:", mediadir)
#         image_files = glob(os.path.join(mediadir, "image*"))
#         image_files = [fn for fn in image_files if ffilter(fn)]
#         print("\nConverting image files...")
#         for imgfn in image_files:
#             old_img_fsize = os.path.getsize(imgfn)
#             print("Converting %r (%s kb)..." % (imgfn,  old_img_fsize//1024))
#             fnbase, fnext = os.path.splitext(imgfn)
#             if fnext == '.jpg' or fnext == '.jpeg':
#                 print(" - Preserving JPEG image format for file %r." % (imgfn,))
#                 outputfn = imgfn
#             else:
#                 outputfn = fnbase + output_ext
#             img = Image.open(imgfn)
#             if img_max_size and (img.height > img_max_size or img.width > img_max_size):
#                 downscalefactor = (max(img.size) // img_max_size) + 1
#                 newsize = tuple(v // downscalefactor for v in img.size)
#                 if verbose and verbose > 1:
#                     print(" - Resizing %sx, from %s to %s" % (downscalefactor, img.size, newsize))
#                 img.resize(newsize)
#             # extra/unused kwargs to Image.save are silently ignored (e.g. `quality` for png)
#             if img_mode:
#                 if verbose and verbose > 1:
#                     print(" - Changing image mode from %s to %s (fill color: %s)..." % (img_mode, img.mode, fill_color))
#                 if fill_color:
#                     # From https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
#                     img.load()  # needed for split()
#                     background = Image.new(img_mode, img.size, fill_color)
#                     background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
#                     img = background
#                 else:
#                     img = img.convert(img_mode)
#             try:
#                 img.save(outputfn, optimize=optimize, quality=quality)
#             except OSError as e:
#                 if on_error == "continue":
#                     print(" - ERROR saving image, skipping!")
#                     continue
#                 else:
#                     raise e
#             print(" - Saved:  %r (%s kb)" % (outputfn, os.path.getsize(outputfn) // 1024))
#             new_img_fsize = os.path.getsize(outputfn)
#             if fsize_filter and new_img_fsize > fsize_filter and verbose and verbose > 0:
#                 print(" - Notice: Filesize %s kb is still above the filesize limit (%s kb)"
#                       % (new_img_fsize//1024, fsize_filter//1024))
#             if fnext != output_ext:
#                 # We only need to change the basename, all images are in the same directory...
#                 changed_fns.append((os.path.basename(imgfn), os.path.basename(outputfn)))
#                 os.remove(imgfn)
#                 if verbose and verbose > 1:
#                     print(" - Deleted: %r" % (imgfn,))
#         if verbose and verbose > 1:
#             print("\nChanged image filenames:")
#             print("\n".join("  %s -> %s" % tup for tup in changed_fns))

#         if verbose and verbose > 1:
#             print("\nFinding changed .xml.rels files...")
#         xml_files = glob(os.path.join(pptdir, "**", "*.xml.rels"), recursive=True)
#         changed_xml_fns = []
#         for xmlfn in xml_files:
#             with open(xmlfn) as fd:
#                 xml = fd.read()
#                 if any(oldimgfn in xml for oldimgfn, newimgfn in changed_fns):
#                     # Make sure to use '\r\n' as file endings, because Microsoft:
#                     changed_xml_fns.append((xmlfn, xml.replace("\n", "\r\n")))

#         print("\nMaking changes to %s of %s xml relationship files..." % (len(changed_xml_fns), len(xml_files)))
#         # Be a bit more stringent about replacing filenames in the xml (in case we have e.g. externally-linked images)
#         pat_fmt = r'"../media/{}"'
#         for xmlfn, xml in changed_xml_fns:
#             count = 0
#             for oldimgfn, newimgfn in changed_fns:
#                 oldimgpat, newimgpat = pat_fmt.format(oldimgfn), pat_fmt.format(newimgfn)
#                 xml = xml.replace(oldimgpat, newimgpat)
#                 count += 1
#             if verbose and verbose > 1:
#                 print(" - Performed %s substitutions in file %r" % (count, xmlfn))
#             with open(xmlfn, 'w') as fd:
#                 fd.write(xml)

#         if wait_before_zip:
#             print("""\n\nWAITING BEFORE ZIP:  (` --wait-before-zip ` argument was provided)
#                    This gives you an opportunity to make manual changes before zipping the archive.
#                    You can find the unzipped files in the temporary directory:
#                               %s
#                   """ % tmpdirname)
#             input("Press enter to continue...")
#         if os.path.exists(new_zip_fn) and not overwrite:
#             print(("\nNOTICE: Output file already exists. If you want to keep the old file,\n%r,\n"
#                    "please move/rename it before continuing. ") % (new_zip_fn,))
#             input("Press enter to continue... ")
#         print("\nCreating new pptx zip archive: %r" % (new_zip_fn,))
#         zip_directory(tmpdirname, new_zip_fn, relative=True, compress_type=compress_type, verbose=verbose)
#         new_fsize = os.path.getsize(new_zip_fn)
#         print("\nDone! New file size: %0.01f MB (%0.01f %% of original size)"
#               % (new_fsize/2**20, 100*new_fsize/old_fsize))

#         if convert_to == "png" and verbose and verbose > 0:
#             print("""
#                 Notice: This pptx downsizing was done using PNG images (the default setting). 
#                 PNG format preserves the appearance and quality of images very well, 
#                 but may result in large file sizes for complex pictures with lots of fine details. 
#                If you noticed that some files were still excessive in size (in the output above), 
# try running pptx-downsizer again with `--convert-to jpeg` as argument, e.g.: 
#     $ pptx-downsizer "{}" --convert-to jpeg""".format(new_zip_fn))

#     return new_zip_fn

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
        #    doc = aw.Document(user_pr.file.path)
        #    doc.cleanup()

        #    shapes = [node.as_shape() for node in doc.get_child_nodes(aw.NodeType.SHAPE, True)]
        #    for shape in shapes:
        #         if shape.isImage:
        #         # It's up to developer to choose the library for image compression.
        #             image = Image.open(shape.image_data.to_stream())

        # # ...
        #         # Compress image and set it back to the shape.
        #             shape.image_data.set_image("yourCompressedImage")      

        #    save_options = aw.saving.OoxmlSaveOptions
        #    save_options.compression_level = aw.saving.CompressionLevel.MAXIMUM

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

          # file_compress(filename,new_filename)

        #    with zipfile.ZipFile(user_pr.file.path, 'w') as jungle_zip:
        #        jungle_zip.write(filename, compress_type=zipfile.ZIP_DEFLATED)
           #doc.save("Output.docx", save_options)
           return HttpResponse("WORD file compressed successfuly")
    else:  
        print("else1")
        uploadFile = FileForm()  
        print("else2")
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


            # renderer = aw.pdf2word.fixedformats.PdfFixedRenderer()
            # pdf_read_options = aw.pdf2word.fixedformats.PdfFixedOptions()
            # pdf_read_options.image_format = aw.pdf2word.fixedformats.FixedImageFormat.JPEG
            # pdf_read_options.jpeg_quality = 50

            # with open (user_pr.file.path, 'rb') as pdf_stream:
            #     pages_stream = renderer.save_pdf_as_images(pdf_stream, pdf_read_options)

            # builder = aw.DocumentBuilder()
            # for i in range(0, len(pages_stream)):
            #     # Set maximum page size to avoid the current page image scaling.
            #     max_page_dimension = 1584
            #     page_setup = builder.page_setup
            #     set_page_size(page_setup, max_page_dimension, max_page_dimension)

            #     page_image = builder.insert_image(pages_stream[i])

            #     set_page_size(page_setup, page_image.width, page_image.height)
            #     page_setup.top_margin = 0
            #     page_setup.left_margin = 0
            #     page_setup.bottom_margin = 0
            #     page_setup.right_margin = 0

            #     if i != len(pages_stream) - 1:
            #         builder.insert_break(aw.BreakType.SECTION_BREAK_NEW_PAGE)

            # save_options = aw.saving.PdfSaveOptions()
            # save_options.cache_background_graphics = True

            PDFNet.Initialize("demo:1679382800894:7d172aad03000000006e4e8c2e43b0a1edd4e0fe31883bada9d6815484")
            doc = PDFDoc(user_pr.file.path)
        # Optimize PDF with the default settings
            doc.InitSecurityHandler()
        # Reduce PDF size by removing redundant information and compressing data streams
            Optimizer.Optimize(doc)
            filename, ext = os.path.splitext(user_pr.file.path)
            new_filename = f"{filename}_compressed.pdf"
            doc.Save(new_filename, SDFDoc.e_linearized)
            doc.Close()
        #builder.document.save("Output.pdf", save_options)
            return HttpResponse("PDF files compressed successfuly")
    else:  
        print("else1")
        uploadFile = FileForm()  
        print("else2")
    return render(request,"CompressPDF.html",{'form':uploadFile})

def set_page_size(page_setup, width, height):

    page_setup.page_width = width
    page_setup.page_height = height

import os
from pathlib import Path
import tempfile
import glob
import zipfile
from tqdm.contrib.concurrent import process_map

# from utils import (
#      run_command,
#      file_size,
#      human_readable_size,
#      convert_size_to_bytes,
#      which,
#  )


# def _compress_image(quality,input_file,output_file,verbose):
#      cmd = [
#         "convert",
#         "-quality",
#         quality,
#         "-background",
#         "white",
#         "-alpha",
#         "remove",
#         "-alpha",
#         "off",
#         input_file + "[0]",  # add [0] to use only the first page of TIFFs
#         output_file,
#     ]
#      run_command(cmd,verbose)


# def _has_transparency(input_file, verbose=False):
#     cmd = ["identify", "-format", "%[opaque]", input_file]
#     stdout, _ = run_command(cmd, verbose=verbose)
#     if stdout.strip() == "False":
#         return True


# # class CompressPptxError(SystemError):
# #     pass


# # def __init__(
#     #     self,
#     #     input_file: str,
#     #     output_file: str,
#     #     size=convert_size_to_bytes("1MiB"),
#     #     quality=85,
#     #     transparency="",
#     #     skip_transparent_images=False,
#     #     verbose=False,
#     #     force=False,
#     # ) -> None:
# def comp(request):
#         input_file = input_file
#         output_file = output_file
#         size = convert_size_to_bytes("1MiB")
#         quality = 85
#         transparency = "white"
#         skip_transparent_images = False
#         verbose = False
#         force = False

#         image_list = []

#         # for expected_cmd in ["convert", "identify"]:
#         #     if which(expected_cmd) is None:
#         #         raise CompressPptxError(
#         #             f"ImageMagick '{expected_cmd}' not found in PATH. Make sure you have installed ImageMagick and that the '{expected_cmd}' command is available."
#         #         )

#         # if quality < 0 or quality > 100:
#         #     raise CompressPptxError("Quality must be between 0-100!")

#         # if not Path(input_file).exists():
#         #     raise CompressPptxError(f"No such file: {self.input_file}")

#         # if not (
#         #     Path(self.input_file).suffix.endswith("pptx")
#         #     or Path(self.input_file).suffix.endswith("potx")
#         # ):
#         #     raise CompressPptxError("Input must be a PPTX or POTX file!")

#         # if Path(output_file).exists() and not force:
#         #     raise CompressPptxError(
#         #         f"Output file {output_file} already exists. Use -f/--force to force overwriting."
#         #     )

#         temp_dir = None

#         if verbose:
#             print(f"Converting {input_file} to {output_file}")

#         with tempfile.TemporaryDirectory() as temp_dir:
#             temp_dir = temp_dir

#             # Unzip
#             _unzip(input_file,temp_dir,verbose)

#             # Collect compressible files
#             _find_images(temp_dir,size,verbose,quality,transparency,skip_transparent_images,image_list)

#             # Compress
#             _compress_images(image_list,verbose,quality,input_file,output_file,verbose)

#              # Replace rels
#             _replace_rels(temp_dir,verbose,image_list)

#             # Zip back
#             _zip(temp_dir,output_file)

#         if verbose:
#             _print_stats(input_file,output_file)

# def _unzip(input_file,temp_dir,verbose):
#         print("Extracting file ...")
#         with zipfile.ZipFile(input_file, "r") as zip_f:
#             zip_f.extractall(temp_dir)
#             if verbose:
#                 print(f"Extracted temp files to {temp_dir}")

# def _find_images(temp_dir,size,verbose,quality,transparency,skip_transparent_images,image_list):
#         if temp_dir is None:
#             raise RuntimeError("Temp dir not created!")

#         for file in glob.iglob(
#             os.path.join(temp_dir, "ppt", "media", "*"), recursive=True
#         ):
#             # skip unaffected extensions
#             if not (
#                 file.endswith(".png") or file.endswith(".emf") or file.endswith(".tiff")
#             ):
#                 continue

#             # skip files that are too small
#             fsize = file_size(file)
#             if fsize < size:
#                 # print(f"Skipping {Path(file).name} because it is too small")
#                 continue

#             # skip files with transparency
#             if skip_transparent_images and _has_transparency(file, verbose):
#                 if verbose:
#                     print(f"Skipping {Path(file).name} because it contains transparency")
#                 continue

#             if verbose:
#                 print(
#                     f"{Path(file).name} added to conversion queue ({human_readable_size(fsize)})"
#                 )

#             image_list.append(
#                 {
#                     "input": file,
#                     "output": Path(file).parent / (Path(file).stem + "-compressed.jpg"),
#                     "input_size": fsize,
#                     "output_size": None,
#                     "quality": quality,
#                     "transparency": transparency,
#                     "verbose": verbose,
#                 }
#             )

# def _compress_images(image_list,verbose,quality,input_file,output_file):
#         if len(image_list) == 0:
#             print("No images to compress!")
#             return

#         print(f"Compressing {len(image_list)} file(s) ...")

#         for image in image_list:
#             if verbose:
#                 print(f"Compressing {image['input']} to {image['output']}")
#         process_map(_compress_image(quality,input_file,output_file,verbose), image_list)

#         # remove borked files
#         warnings = []
#         for image in image_list:
#             if not Path(image["output"]).exists():
#                 print(f"Warning: could not convert {image['input']}")
#                 warnings.append(image)

#             output_size = file_size(image["output"])
#             image["output_size"] = output_size

# def _zip(temp_dir,output_file) -> None:
#         if temp_dir is None:
#             raise RuntimeError("Temp dir not created!")

#         src_path = Path(temp_dir)
#         with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
#             for file in src_path.rglob("*"):
#                 zf.write(file, file.relative_to(src_path))

#         print(f"Output written to: {output_file}")

# def _print_stats(input_file,output_file) -> None:
#         input_size = file_size(input_file)
#         output_size = file_size(output_file)
#         percentage = round((input_size - output_size) / input_size * 100, 2)
#         print(f"Input file:  {human_readable_size(input_size)}")
#         print(
#             f"Output file: {human_readable_size(output_size)} ({percentage}% reduction)"
#         )

# def _replace_rels(temp_dir,verbose,file_list) -> None:
#         if temp_dir is None:
#             raise RuntimeError("Temp dir not created!")

#         if verbose:
#             print("Replacing metadata ...")

#         for file in glob.iglob(
#             os.path.join(temp_dir, "ppt", "**", "*.rels"), recursive=True
#         ):
#             content = ""
#             with open(str(file)) as f:
#                 content = f.read()

#                 for compress_file in file_list:
#                     original_file = Path(compress_file["input"]).name
#                     target_file = Path(compress_file["output"]).name

#                     if original_file not in content:
#                         continue

#                     content = content.replace(original_file, target_file)

#             with open(str(file), "w") as f:
#                 f.write(content)





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
