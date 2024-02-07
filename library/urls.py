from django.urls import path
from library import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView



urlpatterns = [
path('librarydashboard/', views.librarydashboard,name='librarydashboard'),

 
path('addbook/', views.addbook,name='addbook'),
path('libviewbook/', views.libviewbook,name='libviewbook'),
path('issuebook/', views.issuebook,name='issuebook'),
path('addbook/', views.addbook,name='addbook'),
path('viewissuedbook/', views.viewissuedbook,name='viewissuedbook'),
path('viewstudent/', views.viewstudent,name='viewstudent'),
path('libviewmessage/', views.libviewmessage,name='libviewmessage'),
path('libsentmessage/', views.libsentmessage,name='libsentmessage'),
path('libviewprofile/', views.libviewprofile,name='libviewprofile'),
path('libnewmessage/', views.libnewmessage,name='libnewmessage'),
path('libnoticeboard/', views.libnoticeboard,name='libnoticeboard'),
path('libviewprofile/', views.libviewprofile,name='libviewprofile'),
path('libexamtable/', views.libexamtable,name='libexamtable'),
path('libtemplate1/', views.libtemplate1,name='libtemplate1'),
path('libtemplate2/', views.libtemplate2,name='libtemplate2'),
path('libtemplate3/', views.libtemplate3,name='libtemplate3'),
path('libtemplate4/', views.libtemplate4,name='libtemplate4'),
path('libdeletemessage/<str:pk>/', views.libdeletemessage,name='libdeletemessage'),
path('libstatus/', views.libstatus,name='libstatus'),
path('libviewstatus/', views.libviewstatus,name='libviewstatus'),
path('libdeletestatus/', views.libdeletestatus,name='libdeletestatus'),
path('libtable/', views.libtable,name='libtable'),
path('libexamtable/', views.libexamtable,name='libexamtable'),

path('libchangepassword/', views.libchangepassword,name='libchangepassword'),
path('libCalendarView/', views.libCalendarView.as_view(),name='libCalendarView'),


]
