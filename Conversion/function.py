import xlrd
import pdfplumber
from reportlab.pdfgen import canvas
import img2pdf
from PIL import Image
import pandas as pd
import PyPDF2
from pdf2docx import Converter
from reportlab.lib.pagesizes import letter
from fpdf import FPDF 
from docx import Document

def textTOpdf(input_file,output_file):

    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create a PDF canvas
    pdf = canvas.Canvas(output_file, pagesize=letter)

    # Set the font and size for the text
    pdf.setFont("Helvetica", 12)

    # Set the position to start writing the text
    x = 50
    y = 750

    # Split the input text into lines
    lines = content.split("\n")

    # Calculate the maximum number of lines that can fit on a page
    max_lines_per_page = 50  # Adjust as needed

    # Iterate over the lines and handle pagination
    line_count = 0
    page_number = 1
    for line in lines:
        if line_count >= max_lines_per_page:
            # Create a new page
            pdf.showPage()
            page_number += 1
            line_count = 0
            y = 750

        pdf.drawString(x, y, line)
        y -= 20  # Adjust the y-coordinate for the next line
        line_count += 1

    # Save the PDF document
    pdf.showPage()  # Add the page to the PDF
    pdf.save()

def pdfTOtext(input_file,output_file):
    PdfFileObject = open(input_file, 'rb')
    output_file = open(output_file, "w", encoding="utf-8")
    pdfReader = PyPDF2.PdfReader(PdfFileObject)
    numOfPages = len(pdfReader.pages)

    for i in range(numOfPages):
        page = pdfReader.pages[i]
        text = page.extract_text()
        output_file.write(text)

    output_file.close()    
    PdfFileObject.close()

def pdfTOexcel(input_file,output_file):
    # Open the PDF file using pdfplumber
    with pdfplumber.open(input_file) as pdf:
        # Create a list to store the extracted lines
        extracted_lines = []
        
        # Iterate through each page of the PDF
        for page in pdf.pages:
            # Extract text from the page and split into lines
            lines = page.extract_text().split('\n')
            
            # Append each line to the extracted_lines list
            extracted_lines.extend(lines)
    
    # Determine the number of columns dynamically based on the maximum line length
    max_line_length = max(len(line.split()) for line in extracted_lines)
    
    # Create a list of column names
    column_names = [f"Column{i+1}" for i in range(max_line_length)]
    
    # Create an empty DataFrame with the determined column names
    df = pd.DataFrame(columns=column_names)
    
    # Populate the DataFrame with the extracted lines
    for line in extracted_lines:
        # Split the line into columns based on whitespace separator
        columns = line.split()
        
        # Pad the columns list with None values if the length is less than max_line_length
        columns.extend([None] * (max_line_length - len(columns)))
        
        # Add the row to the DataFrame
        df = df.append(pd.Series(columns, index=df.columns), ignore_index=True)
    
    # Write the DataFrame to an Excel file
    df.to_excel(output_file, index=False)			
    
def excelTOpdf(input_file,output_file):
    # Load the .xls file using xlrd
    workbook = xlrd.open_workbook(input_file)
    sheet = workbook.sheet_by_index(0)  # Assuming the first sheet is to be converted
    
    # Create the PDF object
    pdf = FPDF()

    # Add a page to the PDF
    pdf.add_page()
    
    # Set the font and font size for the PDF
    pdf.set_font("Arial", size=12)
    
    # Iterate through each row and column, adding cell values to PDF
    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            cell_value = sheet.cell_value(row, col)
            pdf.cell(40, 10, str(cell_value))
        pdf.ln()  # Move to the next line
    
    # Save the PDF file
    pdf.output(output_file)

def pdfTOword(input_file,output_file):
    cv = Converter(input_file)
    cv.convert(output_file, start = 0, end = None)
    cv.close()

def wordTOpdf(input_file,output_file):
    # Load the Word document
    doc = Document(input_file)

    # Create a PDF canvas
    pdf = canvas.Canvas(output_file, pagesize=letter)

    y = 750  # Initial y-position for the first line

    for paragraph in doc.paragraphs:
        # Add each line from the Word document to the PDF
        pdf.drawString(10, y, paragraph.text)  # Adjust the position as needed
        y -= 12  # Adjust the y-position for the next line

    # Save the PDF document
    pdf.save()
    
def imageTOpdf(input_file,output_file):
    image = Image.open(input_file)  # opening image
    pdf_bytes = img2pdf.convert(image.filename)   # converting into chunks using img2pdf

    with open(output_file, "wb") as file:      #write file 
        file.write(pdf_bytes)

    image.close()    # closing image file
    input_file.close()     # closing pdf file
