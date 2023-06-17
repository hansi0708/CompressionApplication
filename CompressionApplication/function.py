import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pyrebase

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

def firebase_data(request):
    idToken=request.session['uid']
    a=authe.get_account_info(idToken)
    a=a['users']
    a=a[0]
    a=a['localId']

    FirstName = database.child('users').child(a).child('FirstName').get().val()
    LastName = database.child('users').child(a).child('LastName').get().val()
    return {"FirstName":FirstName,"LastName":LastName}


#GET FILE SIZE FORMAT 		
def get_size_format(b, factor=1024, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"