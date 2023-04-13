from django.shortcuts import render

def welcome(request):
	return render(request,"Welcome.html")

def compress(request):
	return render(request,"Compression.html")