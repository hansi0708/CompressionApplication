import os
import platform
from django.shortcuts import render
import pyrebase
from datetime import datetime
from django.http.response import HttpResponse
import pyrebase
import firebase_admin
from firebase_admin import credentials, storage
from django.contrib import messages


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


# Create your views here.
def check(request):
	all_users=database.child('users').shallow().get().val()
	list_users=[]

	for i in all_users:                                              
		list_users.append(i)
	
	print(list_users)
	#list_users.sort(reverse=True) when time stamp based sorting

	names=[]
	for i in list_users:
		name=database.child('users').child(i).child('name').get().val()
		names.append(name)

	print(names)

	centres=[]
	for i in list_users:
		centre=database.child('users').child(i).child('centre').get().val()
		centres.append(centre)

	print(centres)

	departments=[]
	for i in list_users:
		department=database.child('users').child(i).child('department').get().val()
		departments.append(department)

	print(departments)
	
	comb_list=zip(list_users,names,centres,departments)	
		    
	return render(request,"ListUsers.html",{'comb_list':comb_list})

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

		for i in comp_list:   
			filename=database.child('compression').child(i).child('file_name').get().val()                                           
			filenames.append(filename)

		for i in all_user_comp:  
			time=database.child('compression').child(i).child('date_time').get().val()                                            
			times.append(time)

		for i in times:
			dat=datetime.fromtimestamp(i)
			date.append(dat)
		
		comb_list=zip(times,comp_list,filenames,date)

	else:
		comb_list=[]	
	
	return render(request,"UserCompList.html",{'comb_list':comb_list,'FirstName':FirstName,'LastName':LastName})

def comp_details(request):
	comp_id=request.GET.get('z')
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

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
	    'dat':dat,
		'FirstName':FirstName,
		'LastName':LastName
    }

	return render(request,"CompDetails.html",context)

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
		
		for i in conv_list:   
			filename=database.child('conversion').child(i).child('file_name').get().val()                                           
			filenames.append(filename)
		
		for i in all_user_conv:  
			time=database.child('conversion').child(i).child('date_time').get().val()                                            
			times.append(time)
		
		for i in times:
			dat=datetime.fromtimestamp(i)
			date.append(dat)
		
		comb_list=zip(times,conv_list,filenames,date)	

	else:
		comb_list=[]
	
	return render(request,"UserConvList.html",{'comb_list':comb_list,'FirstName':FirstName,'LastName':LastName})

def conv_details(request):
	conv_id=request.GET.get('z')
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']
	FirstName = database.child('users').child(a).child('FirstName').get().val()
	LastName = database.child('users').child(a).child('LastName').get().val()

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
	    'FirstName':FirstName,
		'LastName':LastName
    }

	return render(request,"ConvDetails.html",context) 


#GET FILE SIZE
def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
