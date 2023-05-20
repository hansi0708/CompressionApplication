from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.signIn),
    path('postsignIn/', views.postsignIn),

    path('signUp/', views.signUp, name="signup"),
    path('postsignUp/', views.postsignUp),

    path('logout/', views.logout, name="log"),

    path('updateProfile/',views.updateProfile),

    path('forgot/', views.forgot),

    path('resetPassword/',views.adResetPassword),
    path('postReset/',views.postReset),

    path('dashboard/', views.adDashboard),
    path('userProfile/',views.adProfile),

    #Comp url
    path('userCompList/',views.adCompList),
    #path('comp_details/',views.comp_details),

    #Conv url
    path('userConvList/',views.adConvList),
    #path('conv_details/',views.conv_details),

    path('listUsers/',views.listUsers),

    ]