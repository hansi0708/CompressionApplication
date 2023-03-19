from django.shortcuts import render
from firebase_admin import db

def welcome(request):
	return render(request,"Welcome.html")

def home(request):
	return render(request,"Home.html")

def compress(request):
	return render(request,"Compression.html")



	# idToken=request.session['uid']
	# if(idToken!= None):
	#     return render(request,"Login.html")
	# else:


		
	