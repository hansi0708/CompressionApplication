import sys
import zipfile
import zlib
import PyPDF2
from PIL import Image

def compress_word(input_file,output_file):
    
    with open(input_file, mode="rb") as fin, open(output_file, mode="wb") as fout:
        data = fin.read()
        compressed_data = zlib.compress(data, zlib.Z_BEST_COMPRESSION)
        print(f"Original size: {sys.getsizeof(data)}")

        # Original size: 1000033
        print(f"Compressed size: {sys.getsizeof(compressed_data)}")

        # Compressed size: 1024
        fout.write(compressed_data)

def compress_image(input_file,output_file):
    #Image compression code
    quality=90
            
    # Open the image file
    img = Image.open(input_file)
    try:
                #Save the image with the corresponding quality and optimize set to True
        img.save(output_file, quality=quality, optimize=True)

    except OSError:
        #Convert the image to RGB mode first
        img = img.convert("RGB")

        #Save the image with the corresponding quality and optimize set to True
        img.save(output_file, quality=quality, optimize=True)
    
    img.close()

def compress_ppt(input_file,output_file):
    with zipfile.ZipFile(output_file, 'w') as jungle_zip:
        jungle_zip.write(input_file, compress_type=zipfile.ZIP_DEFLATED)

def compress_pdf(input_file,output_file):
    
    with open(input_file, 'rb') as input_file, open(output_file, 'wb') as output_file:
        
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.compress_content_streams()  # Compress the content streams of the page
            pdf_writer.add_page(page)

        pdf_writer.write(output_file)