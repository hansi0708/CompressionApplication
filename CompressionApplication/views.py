from django.shortcuts import render

def welcome(request):
	return render(request,"Welcome.html")

def home(request):
	return render(request,"Home.html")

def compress(request):
	return render(request,"Compression.html")