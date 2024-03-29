from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.signIn),
    path('postsignIn/', views.postsignIn),

    path('signUp/', views.signUp, name="signup"),
    path('postsignUp/', views.postsignUp),

    path('home/', views.home, name="home"),
    
    path('logout/', views.logout, name="log"),

    path('updateProfile/',views.updateProfile),
    path('postUpdate/',views.postUpdate),

    path('forgot/', views.forgot),
    path('postForgot/',views.postForgot),

    path('resetPassword/',views.resetPassword),
    path('postReset/',views.postReset),
    
    path('dashboard/', views.dashboard),
    path('userProfile/',views.userProfile),

    #Comp url
    path('userCompList/',views.userCompList),
    path('comp_details/',views.comp_details),
    path('orgDownload/',views.orgCompDow),
    path('compDownload/',views.compDow),

    #Conv url
    path('userConvList/',views.userConvList),
    path('conv_details/',views.conv_details),
    path('orDownload/',views.orgConvDow),
    path('convDownload/',views.convDow),

    path('comp_arch/',views.comp_arch),
    path('conv_arch/',views.conv_arch),
    path('archive/',views.archive),

    path('del_arc_cmp/',views.del_arc_cmp),
    path('del_arc_cnv/',views.del_arc_cnv),

    # path('conv_arch/',views.conv_arch),
    # path('conv_arc_list/',views.conv_arc_list),

    ]