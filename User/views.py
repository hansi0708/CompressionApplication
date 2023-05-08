import os
import platform
from django.shortcuts import render
import pyrebase
from datetime import datetime
from django.http.response import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, storage

#FIREBASE CONFIG
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

# cred=credentials.Certificate('serviceAccountKey.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': "compression-tool-6af95.appspot.com"
# })


# Initialising database, auth, firebase and storage   
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage=firebase.storage()


#HOME
def home(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()
	return render(request,"Home.html",{"FirstName":FirstName,"LastName":LastName})


#SIGN IN
def signIn(request):
	return render(request,"Login.html")

def postsignIn(request):

	email=request.POST.get('email')
	pasw=request.POST.get('password')

	try:
		
		#If there is no error then signin the user with given email and password
		user=authe.sign_in_with_email_and_password(email,pasw)

	except:

		message="Invalid Credentials!!Please Check your Data"
		return render(request,"Login.html",{"message":message})
	
	session_id=user['idToken']
	request.session['uid']=str(session_id)
	print(session_id)
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()
	return render(request,"Home.html",{"email":email,"FirstName":FirstName,"LastName":LastName})


#LOGOUT
def logout(request):

	try:
		del request.session['uid']

	except:
		pass

	return render(request,"Login.html")


#SIGN UP
def signUp(request):
	return render(request,"Registration.html")

def postsignUp(request):

	email = request.POST.get('email')
	passs = request.POST.get('password')
	name = request.POST.get('Salutation')
	FirstName=request.POST.get('FirstName')
	LastName=request.POST.get('LastName')
	designation=request.POST.get('designation')
	department=request.POST.get('department')
	employment_type=request.POST.get('employment_type')
	MiddleName=request.POST.get('MiddleName')

	try:
		
		#Creating a user with the given email and password
		user=authe.create_user_with_email_and_password(email,passs)
		
		uid = user.get('localId')

		data={
			'email':email,
			'Salutation' : name,
			'FirstName':FirstName,
			'LastName':LastName,
			'MiddleName':MiddleName,
			'designation':designation,
			'department':department,
			'employment_type':employment_type
		}

		print("before registration")
		database.child('users').child(uid).set(data)
		print("Success")
		print(uid)

	except:
		return render(request, "Registration.html")
	
	return render(request,"Login.html")


#UPDATE PROFILE
def updateProfile(request):
	
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	salutation = database.child('users').child(a).child('Salutation').get().val()
	MiddleName = database.child('users').child(a).child('MiddleName').get().val()
	department = database.child('users').child(a).child('department').get().val()
	designation = database.child('users').child(a).child('designation').get().val()
	email = database.child('users').child(a).child('email').get().val()
	employment_type = database.child('users').child(a).child('employment_type').get().val()
	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

	context = {
        'Salutation':salutation,
	    'MiddleName':MiddleName,
	    'department':department,
	    'designation':designation,
	    'email':email,
	    'employment_type':employment_type,
	    'FirstName':FirstName,
	    'LastName':LastName 
    }

	return render(request,"UpdateProfile.html",context)

def postUpdate(request):
	email = request.POST.get('email')
	name = request.POST.get('Salutation')
	FirstName=request.POST.get('FirstName')
	LastName=request.POST.get('LastName')
	designation=request.POST.get('designation')
	department=request.POST.get('department')
	employment_type=request.POST.get('employment_type')
	MiddleName=request.POST.get('MiddleName')

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	data={
			'email':email,
			'Salutation' : name,
			'FirstName':FirstName,
			'LastName':LastName,
			'MiddleName':MiddleName,
			'designation':designation,
			'department':department,
			'employment_type':employment_type
		}
	
	database.child('users').child(a).update(data)

	return render(request,"UserProfile.html",data)


#RESET PASSWORD
def resetPassword(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']
	email = database.child('users').child(a).child('email').get().val()

	return render(request,"ResetPassword.html",{'email':email})

def postReset(request):
	email = request.POST.get('email')
	print(email)
	try:
		authe.send_password_reset_email(email)
		message  = "A email to reset password is successfully sent"
		return render(request, "ResetPassword.html", {"message":message})
	except:
		message  = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "ResetPassword.html", {"message":message})


#DASHBOARD
def dashboard(request):
	comp_id=request.GET.get('z')

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

	all_user_comp=database.child('compression').shallow().get().val()
	
	list_comp=[]
	for i in all_user_comp:                                              
		list_comp.append(i)
	
	print(list_comp)

	comp_list=[]
	for i in list_comp:
		comp=database.child('compression').child(i).child('user_id').get().val()
		if comp == a: comp_list.append(i)
		
	filenames=[]
	for i in comp_list:   
		filename=database.child('compression').child(i).child('file_name').get().val()                                           
		filenames.append(filename)

	all_user_conv=database.child('conversion').shallow().get().val()
	
	list_conv=[]
	for i in all_user_conv:                                              
		list_conv.append(i)
	
	conv_list=[]
	for i in list_conv:
		conv=database.child('conversion').child(i).child('user_id').get().val()
		if conv == a: conv_list.append(i)


	
	times=[]
	for i in all_user_comp:  
		time=database.child('compression').child(i).child('date_time').get().val()                                            
		times.append(time)

	date=[]
	for i in times:
		i=float(i)
		dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
		date.append(dat)

	# months=[]
	# for i in date:
	# 	# i=int(i)
	# 	month=datetime.strftime('%m-%Y')
	# 	months.append(month)

	context = {
		  'FirstName':FirstName,
		  'LastName':LastName,
	      'count_comp':len(comp_list),
	      'count_conv':len(conv_list)
    }

	return render(request,"UserDashboard.html",context)



#PROFILE
def userProfile(request):

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	salutation = database.child('users').child(a).child('Salutation').get().val()
	MiddleName = database.child('users').child(a).child('MiddleName').get().val()
	department = database.child('users').child(a).child('department').get().val()
	designation = database.child('users').child(a).child('designation').get().val()
	email = database.child('users').child(a).child('email').get().val()
	employment_type = database.child('users').child(a).child('employment_type').get().val()
	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

	context = {
        'Salutation':salutation,
	    'MiddleName':MiddleName,
	    'department':department,
	    'designation':designation,
	    'email':email,
	    'employment_type':employment_type,
	    'FirstName':FirstName,
	    'LastName':LastName 
    }
	
	return render(request,"UserProfile.html",context)


#COMPRESSION DATA
def userCompList(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

	all_user_comp=database.child('compression').shallow().get().val()
	print(all_user_comp)
	list_comp=[]

	for i in all_user_comp:                                              
		list_comp.append(i)
	
	print(list_comp)

	comp_list=[]
	for i in list_comp:
		comp=database.child('compression').child(i).child('user_id').get().val()
		if comp == a: comp_list.append(i)

	print(comp_list)

	filenames=[]
	for i in comp_list:   
		filename=database.child('compression').child(i).child('file_name').get().val()                                           
		filenames.append(filename)

	times=[]
	for i in all_user_comp:  
		time=database.child('compression').child(i).child('date_time').get().val()                                            
		times.append(time)

	date=[]
	for i in times:
		i=float(i)
		dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
		date.append(dat)
	
	comb_list=zip(times,comp_list,filenames,date)	
	
	return render(request,"UserCompList.html",{'comb_list':comb_list,'FirstName':FirstName,'LastName':LastName})

def comp_details(request):
	comp_id=request.GET.get('z')
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	filename=database.child('compression').child(comp_id).child('file_name').get().val()
	file_type=database.child('compression').child(comp_id).child('file_type').get().val()
	file_size=database.child('compression').child(comp_id).child('file_size').get().val()
	new_file_size=database.child('compression').child(comp_id).child('new_file_size').get().val()
	time=database.child('compression').child(comp_id).child('date_time').get().val()

	i=float(str(time))
	dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')

	context = {
		'comp_id':comp_id,
        'filename':filename,
	    'file_type':file_type,
	    'file_size':get_size_format(file_size),
	    'new_file_size':get_size_format(new_file_size),
	    'dat':dat
    }

	return render(request,"CompDetails.html",context)

def orgCompDow(request):
    comp_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    
    file_name=database.child('compression').child(comp_id).child('file_name').get().val()
    org_url=database.child('compression').child(comp_id).child('file').get().val()
    if platform.system() == "Windows": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).download(org_url,os.path.expanduser('~\\Downloads\\' +file_name)) 
    elif platform.system() == "Linux" : storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).download(org_url,os.path.expanduser('~/Downloads/'+file_name))
    
	
    # html = "<html><body>.File downloaded successfully</body></html>"
    
    return HttpResponse(".")
    

def compDow(request):
    comp_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    new_file_name=database.child('compression').child(comp_id).child('new_file_name').get().val()
    new_url=database.child('compression').child(comp_id).child('new_file').get().val()
    
    if platform.system() == "Windows": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~\\Downloads\\' +new_file_name)) 
    elif platform.system() == "Linux": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~/Downloads/'+new_file_name))
    
    return HttpResponse("File downloaded successfully") 


#CONVERSION DATA
def userConvList(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

	all_user_conv=database.child('conversion').shallow().get().val()
	list_conv=[]

	for i in all_user_conv:                                              
		list_conv.append(i)
	
	print(list_conv)

	conv_list=[]
	for i in list_conv:
		conv=database.child('conversion').child(i).child('user_id').get().val()
		if conv == a: conv_list.append(i)

	filenames=[]
	for i in conv_list:   
		filename=database.child('conversion').child(i).child('file_name').get().val()                                           
		filenames.append(filename)

	times=[]
	for i in all_user_conv:  
		time=database.child('conversion').child(i).child('date_time').get().val()                                            
		times.append(time)

	date=[]
	for i in times:
		i=float(i)
		dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
		date.append(dat)
	
	comb_list=zip(times,conv_list,filenames,date)	
	
	return render(request,"UserConvList.html",{'comb_list':comb_list,'FirstName':FirstName,'LastName':LastName})

def conv_details(request):
	conv_id=request.GET.get('z')
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	filename=database.child('conversion').child(conv_id).child('file_name').get().val()
	file_type=database.child('conversion').child(conv_id).child('file_type').get().val()
	file_size=database.child('conversion').child(conv_id).child('file_size').get().val()
	new_file_type=database.child('conversion').child(conv_id).child('new_file_type').get().val()
	time=database.child('conversion').child(conv_id).child('date_time').get().val()

	i=float(str(time))
	dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')

	context = {
		'conv_id':conv_id,
        'filename':filename,
	    'file_type':file_type,
	    'file_size':get_size_format(file_size),
	    'new_file_type':new_file_type,
	    'dat':dat
    }

	return render(request,"ConvDetails.html",context) 

def orgConvDow(request):
    conv_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    
    file_name=database.child('conversion').child(conv_id).child('file_name').get().val()
    org_url=database.child('conversion').child(conv_id).child('file').get().val()
    if platform.system() == "Windows": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).download(org_url,os.path.expanduser('~\\Downloads\\'+file_name))
    elif platform.system() == "Linux": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).download(org_url,os.path.expanduser('~/Downloads/'+file_name))
    return HttpResponse("File downloaded successfuly")

def convDow(request):
    conv_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    new_file_name=database.child('conversion').child(conv_id).child('new_file_name').get().val()
    new_url=database.child('conversion').child(conv_id).child('new_file').get().val()
    if platform.system() == "Windows": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~\\Downloads\\'+new_file_name))
    elif platform.system() == "Linux": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~/Downloads/'+new_file_name))
    return HttpResponse("File downloaded successfuly") 

#FORGOT PASSWORD
def forgot(request):
    # idToken=request.session['uid']
    # a=authe.get_account_info(idToken)
    # a=a['users']
    # a=a[0]
    # a=a['localId']
    # email = database.child('users').child(a).child('email').get().val()
    return render(request,"ForgotPass.html")

def postForgot(request):
	email = request.POST.get('email')
	print(email)
	try:
		authe.send_password_reset_email(email)
		message  = "A email to recover password is successfully sent"
		return render(request, "ForgotPass.html", {"message":message})
	except:
		message  = "Something went wrong, Please check the email you provided is registered or not"
		return render(request, "ForgotPass.html", {"message":message})
	

#GET FILE SIZE
def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"

