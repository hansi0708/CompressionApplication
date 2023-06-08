import PyPDF2
from PIL import Image
import heapq
import os

import numpy as np


def compress_word(input_file,output_file):
    with open(input_file, 'rb') as file:
        input_data = file.read()

    compressed_data = []
    count = 1

    for i in range(1, len(input_data)):
        if input_data[i] == input_data[i-1]:
            count += 1
        else:
            compressed_data.append(input_data[i-1])
            compressed_data.append(min(count, 255))
            count = 1

    # Append the last character and count
    compressed_data.append(input_data[-1])
    compressed_data.append(count)

    with open(output_file, 'wb') as file:
        file.write(bytes(compressed_data))


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

def compress_pdf(input_file,output_file):
    
    with open(input_file, 'rb') as input_file, open(output_file, 'wb') as output_file:
        
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            page.compress_content_streams()  # Compress the content streams of the page
            pdf_writer.add_page(page)

        pdf_writer.write(output_file)