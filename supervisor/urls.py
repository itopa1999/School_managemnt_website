from django.urls import path
from supervisor import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
path('supervisordashboard/', views.supervisordashboard,name='supervisordashboard'),
path('supexamrecord/', views.supexamrecord,name='supexamrecord'),
path('supviewfaculty/', views.supviewfaculty,name='supviewfaculty'),
path('supfaculty/<str:pk_profile2>/', views.supfaculty,name='supfaculty'),
path('supviewdepartment/', views.supviewdepartment,name='supviewdepartment'),
path('supdepartment/<str:pk_profile3>/', views.supdepartment,name='supdepartment'),
path('supalllecturers/', views.supalllecturers,name='supalllecturers'),
path('supallstudents/', views.supallstudents,name='supallstudents'),
path('supviewcourse/', views.supviewcourse,name='supviewcourse'),
path('supeviewcourse/<str:pk>/', views.supeviewcourse,name='supeviewcourse'),
path('supnoticeboard/', views.supnoticeboard,name='supnoticeboard'),
path('supnewmessage/', views.supnewmessage,name='supnewmessage'),
path('supviewmessage/', views.supviewmessage,name='supviewmessage'),
path('supsentmessage/', views.supsentmessage,name='supsentmessage'),
path('supexamtable/', views.supexamtable,name='supexamtable'),
path('supCalendarView/', views.supCalendarView.as_view(),name='supCalendarView'),
path('supviewprofile/', views.supviewprofile,name='supviewprofile'),
path('supstatus/', views.supstatus,name='supstatus'),
path('supviewstatus/', views.supviewstatus,name='supviewstatus'),
path('malpractice/', views.malpractice,name='malpractice'),
path('malpractice/', views.malpractice,name='malpractice'),
path('malpractice/', views.malpractice,name='malpractice'),
path('malpractice/', views.malpractice,name='malpractice'),
path('suptemplate1/', views.suptemplate1,name='suptemplate1'),
path('suptemplate2/', views.suptemplate2,name='suptemplate2'),
path('suptemplate3/', views.suptemplate3,name='suptemplate3'),
path('suptemplate4/', views.suptemplate4,name='suptemplate4'),
path('supdeletemessage/<str:pk>/', views.supdeletemessage,name='supdeletemessage'),
path('supdeletestatus/', views.supdeletestatus,name='supdeletestatus'),



path('supchangepassword/', views.supchangepassword,name='supchangepassword'),


]