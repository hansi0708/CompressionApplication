from django.shortcuts import render
from firebase_admin import db
import pyrebase



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

# Initialising database,auth and firebase for further use
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


#import firebase_admin
#from firebase_admin import credentials

#cred = credentials.Certificate("serviceAccountKey.json")
#firebase_admin.initialize_app(cred,
#			      {'databaseURL': 'https://compression-tool-6af95-default-rtdb.firebaseio.com/'
#	  })


#ref = db.reference("dummy.json")


#import json
#with open("dummy.json", "r") as f:
#	file_contents = json.load(f)
#ref.set(file_contents)

def welcome(request):
	return render(request,"Welcome.html")

def home(request):
	return render(request,"Home.html")

def signIn(request):
	return render(request,"Login.html")

def postsignIn(request):
	email=request.POST.get('email')
	pasw=request.POST.get('pass')
	try:
		# if there is no error then signin the user with given email and password
		user=authe.sign_in_with_email_and_password(email,pasw)
	except:
		message="Invalid Credentials!!Please ChecK your Data"
		return render(request,"Login.html",{"message":message})
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	return render(request,"Home.html",{"email":email})

def logout(request):
	try:
		del request.session['uid']
	except:
		pass
	return render(request,"Login.html")

def signUp(request):
	return render(request,"Registration.html")

def postsignUp(request):
	email = request.POST.get('email')
	passs = request.POST.get('pass')
	name = request.POST.get('name')
	try:
		# creating a user with the given email and password
		user=authe.create_user_with_email_and_password(email,passs)
		uid = user['localId']
		idtoken = request.session['uid']
		print(uid)
	except:
		return render(request, "Registration.html")
	return render(request,"Login.html")

def compress(request):
	return render(request,"Compression.html")

