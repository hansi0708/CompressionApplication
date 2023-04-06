from django.shortcuts import render
from firebase_admin import auth
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

# Initialising database, auth and firebase
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


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
	passs = request.POST.get('password')
	name = request.POST.get('name')
	centre=request.POST.get('centre')
	staff=request.POST.get('staff')
	designation=request.POST.get('designation')
	department=request.POST.get('department')
	employment_type=request.POST.get('employment_type')
	level=request.POST.get('level')

	try:
		
		#Creating a user with the given email and password
		user=authe.create_user_with_email_and_password(email,passs)
		
		uid = user.get('localId')

		data={
			'email':email,
			'name':name,
			'centre':centre,
			'staff':staff,
			'designation':designation,
			'department':department,
			'employment_type':employment_type,
			'level':level
		}
		print("before registration")
		database.child('users').push(uid)
		print("ID pushed")
		database.child('users').child(uid).set(data)
		print("Success")
		print(uid)

	except:
		return render(request, "Registration.html")
	
	return render(request,"Login.html")

def profile(request):

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']
	name = database.child('users').child(a).child('name').get().val()
	print(name)

	all_user_comp=database.child('compression').shallow().get().val()
	list_comp=[]

	for i in all_user_comp:                                              
		list_comp.append(i)
	
	print(list_comp)

	comp_list=[]
	for i in list_comp:
		comp=database.child('compression').child(i).child('user_id').get().val()
		if comp == a: comp_list.append(i)

	context = {
          'name':name,
	      'count_comp':len(comp_list)
    }

	return render(request,"UserDashboard.html",context)

def userProfile(request):

	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

	name = database.child('users').child(a).child('name').get().val()
	centre = database.child('users').child(a).child('centre').get().val()
	department = database.child('users').child(a).child('department').get().val()
	designation = database.child('users').child(a).child('designation').get().val()
	email = database.child('users').child(a).child('email').get().val()
	employment_type = database.child('users').child(a).child('employment_type').get().val()
	level = database.child('users').child(a).child('level').get().val()
	staff = database.child('users').child(a).child('staff').get().val()

	context = {
        'name':name,
	    'centre':centre,
	    'department':department,
	    'designation':designation,
	    'email':email,
	    'employment_type':employment_type,
	    'level':level,
	    'staff':staff 
    }
	
	return render(request,"UserProfile.html",context)

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

def userConvList(request):
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
		    
	return render(request,"UserConvList.html",{'comb_list':comb_list})

def userCompList(request):
	idToken=request.session['uid']
	a=authe.get_account_info(idToken)
	a=a['users']
	a=a[0]
	a=a['localId']

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

	times=[]
	for i in all_user_comp:  
		time=database.child('compression').child(i).child('date_time').get().val()                                            
		times.append(time)
	
	comb_list=zip(comp_list,filenames,times)	
	
	return render(request,"UserCompList.html",{'comb_list':comb_list})