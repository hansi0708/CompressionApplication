from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('home/', views.home, name="home"),
    path('signUp/', views.signUp, name="signup"),
    path('', views.signIn),
    path('postsignIn/', views.postsignIn),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('profile/', views.profile),
    path('userProfile/',views.userProfile),
    path('usersList/',views.check),
    path('userConvList/',views.userConvList),
    path('userCompList/',views.userCompList),
    path('details/',views.details),
    path('orgDownload/',views.oDow),
    path('compDownload/',views.cDow),
    path('forgot/', views.forgot),

    ]