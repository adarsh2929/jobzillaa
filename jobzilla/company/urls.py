"""jobzilla URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Add an import:  from my_app/company import views
from company import views

urlpatterns = [
    # path('Chrome url may use '' ',  views.FunctionName    ,  name='Django <form> may use')
     path('home', views.iindex, name='home'),
     path('companies/', views.companies, name='companies'),
     

     path('company-sign/', views.sign, name='company-sign'),
     path('company-signin/', views.signin, name='company-signin'),
     
      path('forgot/', views.forgot, name='forgot'),


     path('reset-password/', views.reset, name='reset-password'),
     path('otp/', views.send_otp, name='otp'),

     path('companyprofile/', views.companyprofile, name='companyprofile'),
     path('profilelogout/', views.profilelogout, name='profilelogout'),


    # Upload karne Company Logo
     path('company-logo', views.company_logo, name='company-logo'),

     path('pfpassword/', views.cprofile_password, name='pfpassword'),


    # Other company profile dekhne.Profile list wala page
    # <int:pk> means "integer may primary key use karge" 
    # All company ku Count karne or Unique id dene
     path('othercompanyprofile/<int:pk>/', views.othercompanyprofile, name='othercompanyprofile'),
     path('companydetail/', views.companydetails, name='companydetails'),
     
     
    # New Job Post 
     path('jobpost/', views.jobposts, name='jobpost'),
     path('jobpostcompanies/', views.jobpostcompanies, name='jobpostcompanies'),
     path('plike/<int:pk>/', views.postlikes, name='plike'),
     
     
     
    # Profile Account Setting
     path('pasetting/', views.pasetting, name='pasetting'),
    # Like data who like
     path('like-jobpost/<int:pk>/', views.like_jobpost, name='like-jobpost'),

# ---------------------------------------------------------------- User ----------------------------------
     path('usup', views.usignup, name='usup'),
     path('user-logo', views.user_logo, name='user-logo'),
     path('uprofile/', views.userprofile, name='uprofile'),
     

     path('userprofilep/', views.userprofilepage, name='userprofilep'),
     
     
     
     path('upassword/', views.profile_password, name='upassword'),
     path('userpasetting/', views.upasetting, name='userpasetting'),
     path('profilelogout/', views.profilelogout, name='profilelogout'),

     path('uallcompanies/', views.allcompanies, name='uallcompanies'),

     path('upost/', views.uposts, name='upost'),
     
]
