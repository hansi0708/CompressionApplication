from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.signUp, name="signup"),
    path('signIn/', views.signIn),
    path('postsignIn/', views.postsignIn),
    path('logout/', views.logout, name="log"),
    path('postsignUp/', views.postsignUp),
    path('profile/', views.profile),
    path('userProfile/',views.userProfile),

    ]