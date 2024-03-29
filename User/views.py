import json
import os
import platform
from django.http import HttpResponseRedirect
from django.shortcuts import render
import pyrebase
from datetime import datetime
import pyrebase
import firebase_admin
from firebase_admin import credentials, storage
from django.contrib import messages
from firebase_admin import auth
from django.core.mail import send_mail

from CompressionApplication.function import get_size_format

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

cred=credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': "compression-tool-6af95.appspot.com"
})


# Initialising database, auth, firebase and storage   
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
storage=firebase.storage()


#HOME
def home(request):
	return render(request,"Home.html")


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
	return render(request,"Home.html",{"email":email})


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

		# Generate the Firebase email verification link
		# user = auth.create_user(email,passs)
		# verification_link = auth.generate_email_verification_link(user.email)

		# # Send the verification link to the user's email
		# send_verification_email(user.email, verification_link)

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

def send_verification_email(email, verification_link):
    subject = 'Verify your email'
    message = f'Click the following link to verify your email: {verification_link}'
    from_email = 'your_email@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


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
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']
	
	if request.method == 'POST':
		email = request.POST.get('email')
		new_password = request.POST.get('new_password')

		try:
			user = auth.get_user_by_email(email)

		except auth.UserNotFoundError:
			error_message = str(auth.UserNotFoundError)
			data = dict()
			messages.error(request, "Error: Something went wrong, Please check the email you provided is registered or not")
			return render(request, "ResetPassword.html", {'message':data})

		auth.update_user(
			a,  # Or you can use email=user.email if you retrieved the user by email
			password=new_password
		)	
			
		data = dict()
		messages.success(request, "Success: An email to reset password is successfully sent ")
		return render(request, "Login.html", {'message':data})
	
	else:
		return render(request, "ResetPassword.html", {'message':data})


#DASHBOARD
def dashboard(request):

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	list_comp=[]
	list_conv=[]
	comp_list=[]
	filenames=[]
	comp_percs=[]
	conv_list=[]
	count_comp=0
	count_conv=0

	all_user_comp=database.child('compression').shallow().get().val()

	if all_user_comp != None:

		for i in all_user_comp:                                              
			list_comp.append(i)

		for i in list_comp:
			comp=database.child('compression').child(i).child('user_id').get().val()
			if comp == a: comp_list.append(i)			
		
		for i in comp_list:   
			filename=database.child('compression').child(i).child('file_name').get().val()                                           
			filenames.append(filename)

		for i in comp_list:   
			comp_perc=database.child('compression').child(i).child('comp_per').get().val()                                           
			comp_percs.append(comp_perc)

		count_comp=len(comp_list)
		# Pair the adjacent elements from the lists
		paired_data = {filenames[i]: comp_percs[i] for i in range(min(len(filenames), len(comp_percs)))}

		# Convert the paired data to JSON
		json_data = json.dumps(paired_data)

	all_user_conv=database.child('conversion').shallow().get().val()

	if all_user_conv != None:
	
		for i in all_user_conv:                                              
			list_conv.append(i)
			
		for i in list_conv:
			conv=database.child('conversion').child(i).child('user_id').get().val()
			if conv == a: conv_list.append(i)
		
		count_conv=len(conv_list)
		
	context = {
		'count_comp':count_comp,
		'count_conv':count_conv,
		'data':json_data
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

	all_user_comp=database.child('compression').shallow().get().val()
	
	list_comp=[]
	comp_list=[]
	filenames=[]
	times=[]
	date=[]

	if all_user_comp != None:

		for i in all_user_comp:                                              
			list_comp.append(i)
		
		for i in list_comp:
			comp=database.child('compression').child(i).child('user_id').get().val()
			if comp == a: comp_list.append(i)

		if comp_list !=None:

			for i in comp_list:   
				filename=database.child('compression').child(i).child('file_name').get().val()                                           
				filenames.append(filename)

			for i in all_user_comp:  
				time=database.child('compression').child(i).child('date_time').get().val()                                            
				times.append(time)

			for i in times:
				date.append(i)
		
			comb_list=zip(times,comp_list,filenames,date)

		else:
			comb_list=[]

	else:
		comb_list=[]	
	
	return render(request,"UserCompList.html",{'comb_list':comb_list})

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
	comp_per=database.child('compression').child(comp_id).child('comp_per').get().val()

	context = {
		'comp_id':comp_id,
        'filename':filename,
	    'file_type':file_type,
	    'file_size':get_size_format(file_size),
	    'new_file_size':get_size_format(new_file_size),
	    'comp_per':comp_per,
	    'dat':time,
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
    
    file_type=database.child('compression').child(comp_id).child('file_type').get().val()
    file_size=database.child('compression').child(comp_id).child('file_size').get().val()
    new_file_size=database.child('compression').child(comp_id).child('new_file_size').get().val()
    time=database.child('compression').child(comp_id).child('date_time').get().val()
    comp_per=database.child('compression').child(comp_id).child('comp_per').get().val()
    i=float(str(time))
    dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    
    if platform.system() == "Windows": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).download(org_url,os.path.expanduser('~\\Downloads\\' +file_name)) 
    elif platform.system() == "Linux" : storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+file_name).download(org_url,os.path.expanduser('~/Downloads/'+file_name))
    data = dict()
    messages.success(request, "Success: Original file downloaded successfully.")
    context = {
		'comp_id':comp_id,
		'filename':file_name,
		'file_type':file_type,
		'file_size':get_size_format(file_size),
		'new_file_size':get_size_format(new_file_size),
		'comp_per':comp_per,
		'dat':dat,
		'message':data,
	}
    return render(request,"CompDetails.html",context)   

def compDow(request):
    comp_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    new_file_name=database.child('compression').child(comp_id).child('new_file_name').get().val()
    new_url=database.child('compression').child(comp_id).child('new_file').get().val()
    file_name=database.child('compression').child(comp_id).child('file_name').get().val()
    file_type=database.child('compression').child(comp_id).child('file_type').get().val()
    file_size=database.child('compression').child(comp_id).child('file_size').get().val()
    new_file_size=database.child('compression').child(comp_id).child('new_file_size').get().val()
    time=database.child('compression').child(comp_id).child('date_time').get().val()
    comp_per=database.child('compression').child(comp_id).child('comp_per').get().val()
    i=float(str(time))
    dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    
    if platform.system() == "Windows": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~\\Downloads\\' +new_file_name)) 
    elif platform.system() == "Linux": storage.child("/comp_files/"+a+"/"+str(comp_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~/Downloads/'+new_file_name))
    
    data = dict()
    messages.success(request, "Success: Compressed file downloaded successfully.")
    context = {
		'comp_id':comp_id,
		'filename':file_name,
		'file_type':file_type,
		'file_size':get_size_format(file_size),
		'new_file_size':get_size_format(new_file_size),
		'comp_per':comp_per,
		'dat':dat,
		'message':data,
	}
    return render(request,"CompDetails.html",context)


#CONVERSION DATA
def userConvList(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	all_user_conv=database.child('conversion').shallow().get().val()
	print(all_user_conv)
	
	list_conv=[]
	conv_list=[]
	filenames=[]
	times=[]
	date=[]

	if all_user_conv != None:

		for i in all_user_conv:                                              
			list_conv.append(i)
		
		for i in list_conv:
			conv=database.child('conversion').child(i).child('user_id').get().val()
			if conv == a: conv_list.append(i)
		
		if conv_list == None:
			comb_list=[]
		
		else :
			
			for i in conv_list:   
				filename=database.child('conversion').child(i).child('file_name').get().val()                                           
				filenames.append(filename)
			
			for i in all_user_conv:  
				time=database.child('conversion').child(i).child('date_time').get().val()                                            
				times.append(time)
			
			for i in times:
				dat=datetime.fromtimestamp(i)
				date.append(dat)
				print(date)
			
			comb_list=zip(times,conv_list,filenames,date)

	else:
		comb_list=[]

	print(comb_list)		
	
	return render(request,"UserConvList.html",{'comb_list':comb_list})

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
	    'dat':dat,
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
    file_type=database.child('conversion').child(conv_id).child('file_type').get().val()
    file_size=database.child('conversion').child(conv_id).child('file_size').get().val()
    new_file_type=database.child('conversion').child(conv_id).child('new_file_type').get().val()
    time=database.child('conversion').child(conv_id).child('date_time').get().val()
    i=float(str(time))
    dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    

    if platform.system() == "Windows": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).download(org_url,os.path.expanduser('~\\Downloads\\'+file_name))
    elif platform.system() == "Linux": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+file_name).download(org_url,os.path.expanduser('~/Downloads/'+file_name))
    data = dict()
    messages.success(request, "Success: Original file downloaded successfully.")
    context = {
		'conv_id':conv_id,
        'filename':file_name,
	    'file_type':file_type,
	    'file_size':get_size_format(file_size),
	    'new_file_type':new_file_type,
	    'dat':dat,
	    'message':data,
	}
    return render(request,"ConvDetails.html",context)

def convDow(request):
    conv_id=request.GET.get('z')
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']
    
    new_file_name=database.child('conversion').child(conv_id).child('new_file_name').get().val()
    new_url=database.child('conversion').child(conv_id).child('new_file').get().val()
    filename=database.child('conversion').child(conv_id).child('file_name').get().val()
    file_type=database.child('conversion').child(conv_id).child('file_type').get().val()
    file_size=database.child('conversion').child(conv_id).child('file_size').get().val()
    new_file_type=database.child('conversion').child(conv_id).child('new_file_type').get().val()
    time=database.child('conversion').child(conv_id).child('date_time').get().val()
    i=float(str(time))
    dat=datetime.fromtimestamp(i).strftime('%H:%M %d-%m-%Y')
    if platform.system() == "Windows": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~\\Downloads\\'+new_file_name))
    elif platform.system() == "Linux": storage.child("/conv_files/"+a+"/"+str(conv_id)+"/"+new_file_name).download(new_url,os.path.expanduser('~/Downloads/'+new_file_name))
    data = dict()
    messages.success(request, "Success: Converted file downloaded successfully.")
    context = {
		'conv_id':conv_id,
        'filename':filename,
	    'file_type':file_type,
	    'file_size':get_size_format(file_size),
	    'new_file_type':new_file_type,
	    'dat':dat,
	    'message':data,
	}
    return render(request,"ConvDetails.html",context)


#FORGOT PASSWORD
def forgot(request):
    return render(request,"ForgotPass.html")

def postForgot(request):
	
	email = request.POST.get('email')
	print(email)
	
	try:
		authe.send_password_reset_email(email)
		data = dict()
		messages.success(request, "Success: An email to reset password is successfully sent ")
		return render(request, "ForgotPass.html", {'message':data})
	
	except:
		messages.error(request, "Error: Something went wrong, Please check the email you provided is registered or not")
		return render(request, "ForgotPass.html", {'message':data})


#ARCHIVE	
def archive(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	selected_option = request.GET.get('selected_option')
	
	filenames=[]
	times=[]
	date=[]
	comb_list=[]
	
	if selected_option == 'convert':
		all_user_conv=database.child('archives').child('conversion').shallow().get().val()
	
		list_conv=[]
		conv_list=[]

		if all_user_conv != None:

			for i in all_user_conv:                                              
				list_conv.append(i)
			
			for i in list_conv:
				conv=database.child('archives').child('conversion').child(i).child('user_id').get().val()
				if conv == a: conv_list.append(i)

			if conv_list != None:
				
				for i in conv_list:   
					filename=database.child('archives').child('conversion').child(i).child('file_name').get().val()                                           
					filenames.append(filename)
				
				for i in all_user_conv:  
					time=database.child('archives').child('conversion').child(i).child('date_time').get().val()                                            
					times.append(time)
				
				now = datetime.now()

				for i in times:
					# ref=database.child('archives').child('conversion').child(i).get().val()
					# parent_ref = ref.parent
					# parent_key = parent_ref.key
					dt=datetime.fromtimestamp(i)
					print(dt)
					dat=now-dt
					print(dat)
					# if dat.days == 7:
					# 	database.child('archives').child('conversion').child(conv_id).remove()
					# else: 
					date.append(7-dat.days)
				
				comb_list=zip(times,conv_list,filenames,date)	

			else:
				comb_list=[]

		else:
			comb_list=[]
	
	else:
		all_user_comp=database.child('archives').child('compression').shallow().get().val()
	
		list_comp=[]
		comp_list=[]

		if all_user_comp != None:

			for i in all_user_comp:                                              
				list_comp.append(i)
			
			for i in list_comp:
				comp=database.child('archives').child('compression').child(i).child('user_id').get().val()
				if comp == a: comp_list.append(i)

			if comp_list !=None:

				for i in comp_list:   
					filename=database.child('archives').child('compression').child(i).child('file_name').get().val()                                           
					filenames.append(filename)

				for i in all_user_comp:  
					time=database.child('archives').child('compression').child(i).child('arc_date').get().val()                                            
					times.append(time)
				
				print(times)
				
				now = datetime.now()
				#now_date=int(datetime.timestamp(now))

				for i in times:
					
					dt=datetime.fromtimestamp(i)
					print(dt)
					dat=now-dt
					print(dat)
					date.append(7-dat.days)
			
				comb_list=zip(times,comp_list,filenames,date)

			else:
				comb_list=[]

		else:
			comb_list=[]

	return render(request,"ArchList.html",{'comb_list':comb_list,'selected_option': selected_option})


#COMP ARCHIVE
def comp_arch(request):
	comp_id=request.GET.get('z')
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	filename=database.child('compression').child(comp_id).child('file_name').get().val()
	new_file_name=database.child('compression').child(comp_id).child('new_file_name').get().val()
	file_type=database.child('compression').child(comp_id).child('file_type').get().val()
	file_size=database.child('compression').child(comp_id).child('file_size').get().val()
	new_file_size=database.child('compression').child(comp_id).child('new_file_size').get().val()
	time=database.child('compression').child(comp_id).child('date_time').get().val()
	org_url=database.child('compression').child(comp_id).child('file').get().val()
	new_url=database.child('compression').child(comp_id).child('new_file').get().val()
	comp_per=database.child('compression').child(comp_id).child('comp_per').get().val()

	now = datetime.now()
	arc_date=int(datetime.timestamp(now))

	data={
		'user_id':a,
		'date_time':time,
		'file_name':filename,
		'new_file_name':new_file_name,
		'file':org_url,
		'file_type':file_type,
		'file_size':file_size,
		'new_file':new_url,
		'new_file_size':new_file_size,
		'comp_per':comp_per,
		'arc_date':arc_date
    }

	database.child('compression').child(comp_id).remove()

	#Storing data in compression table in Firebase Realtime Database
	database.child('archives').child('compression').child(comp_id).set(data)
	
	return HttpResponseRedirect('/archive/') 

def del_arc_cmp(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	comp_id=request.GET.get('z')
	database.child('archives').child('compression').child(comp_id).remove()
	filenames=[]
	times=[]
	date=[]
	comb_list=[]

	all_user_comp=database.child('archives').child('compression').shallow().get().val()
	
	list_comp=[]
	comp_list=[]

	if all_user_comp != None:

		for i in all_user_comp:                                              
			list_comp.append(i)
		
		for i in list_comp:
			comp=database.child('archives').child('compression').child(i).child('user_id').get().val()
			if comp == a: comp_list.append(i)

		if comp_list !=None:

			for i in comp_list:   
				filename=database.child('archives').child('compression').child(i).child('file_name').get().val()                                           
				filenames.append(filename)

			for i in all_user_comp:  
				time=database.child('archives').child('compression').child(i).child('arc_date').get().val()                                            
				times.append(time)
			
			print(times)
			
			now = datetime.now()
			
			for i in times:
				dat=now-i
				date.append(7-dat.days)
		
			comb_list=zip(times,comp_list,filenames,date)

		else:
			comb_list=[]

	else:
		comb_list=[]

	data = dict()
	messages.success(request, "Success: File deleted successfully.")
	context={
		'message':data,
		'comb_list':comb_list,
		'selected_option': 'compress'
	}
	return render(request,"ArchList.html",context)


#CONV ARCHIVE
def conv_arch(request):
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
	org_url=database.child('conversion').child(conv_id).child('file').get().val()
	new_file_name=database.child('conversion').child(conv_id).child('new_file_name').get().val()
	new_url=database.child('conversion').child(conv_id).child('new_file').get().val()

	now = datetime.now()
	arc_date=now
	
	data={
		'user_id':a,
		'date_time':time,
		'file_name':filename,
		'new_file_name':new_file_name,
		'file':org_url,
		'file_type':file_type,
		'file_size':file_size,
		'new_file':new_url,
		'new_file_type':new_file_type,
		'arc_date':arc_date
    }

	database.child('conversion').child(conv_id).remove()

	#Storing data in compression table in Firebase Realtime Database
	database.child('archives').child('conversion').child(conv_id).set(data)
	
	return HttpResponseRedirect('/archive/') 

def del_arc_cnv(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	conv_id=request.GET.get('z')
	database.child('archives').child('conversion').child(conv_id).remove()
	filenames=[]
	times=[]
	date=[]
	comb_list=[]

	all_user_conv=database.child('archives').child('conversion').shallow().get().val()
	
	list_conv=[]
	conv_list=[]

	if all_user_conv != None:

		for i in all_user_conv:                                              
			list_conv.append(i)
		
		for i in list_conv:
			conv=database.child('archives').child('conversion').child(i).child('user_id').get().val()
			if conv == a: conv_list.append(i)

		if conv_list != None:
			
			for i in conv_list:   
				filename=database.child('archives').child('conversion').child(i).child('file_name').get().val()                                           
				filenames.append(filename)
			
			for i in all_user_conv:  
				time=database.child('archives').child('conversion').child(i).child('date_time').get().val()                                            
				times.append(time)
			
			for i in times:
				dat=datetime.fromtimestamp(i)
				date.append(dat)
			
			comb_list=zip(times,conv_list,filenames,date)	

		else:
			comb_list=[]

	else:
		comb_list=[]

	data = dict()
	messages.success(request, "Success: File deleted successfully.")
	context={
		'message':data,
		'comb_list':comb_list,
		'selected_option': 'convert'
	}
	return render(request,"ArchList.html",context)
