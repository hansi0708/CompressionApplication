# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse

from django.shortcuts import render
from .forms import File_Form
from .models import InputFile

def profile(request):
    form = File_Form()
    if request.method == 'POST':
        form = File_Form(request.POST, request.FILES)
        if form.is_valid():
            user_pr = form.save(commit=False)
            user_pr.input_file = request.FILES['input_file']
            file_type = user_pr.input_file.url.split('.')[-1]
            file_type = file_type.lower()
            user_pr.save()
            context=user_pr.objects.all()
            return render(request, 'file.html', {'user_pr': user_pr})
    context = {"form": form,}
    return render(request, 'create.html', context)

def download_file(request,filename):
  # Define Django project base directory
  BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  # Define text file name
  #filename = request.FILES['input_file']
  if filename != '':      
    # Define the full file path
    filepath = BASE_DIR  + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    #return response
    return response(filename, as_attachment=True)

  else: 
    return render(request, 'file.html')

