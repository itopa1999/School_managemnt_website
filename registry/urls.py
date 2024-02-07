from django.urls import path
from registry import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
path('registrydashboard/', views.registrydashboard,name='registrydashboard'),
path('regviewfaculty/', views.regviewfaculty,name='regviewfaculty'),
path('regfaculty/<str:pk_profile2>/', views.regfaculty,name='regfaculty'),
path('regviewdepartment/', views.regviewdepartment,name='regviewdepartment'),
path('regdepartment/<str:pk_profile3>/', views.regdepartment,name='regdepartment'),
path('regalllecturers/', views.regalllecturers,name='regalllecturers'),
path('regallstudents/', views.regallstudents,name='regallstudents'),
path('regviewcourse/', views.regviewcourse,name='regviewcourse'),
path('regdviewcourse/<str:pk>/', views.regdviewcourse,name='regdviewcourse'),
path('regnoticeboard/', views.regnoticeboard,name='regnoticeboard'),
path('regnewmessage/', views.regnewmessage,name='regnewmessage'),
path('regviewmessage/', views.regviewmessage,name='regviewmessage'),
path('regsentmessage/', views.regsentmessage,name='regsentmessage'),
path('regtable/', views.regtable,name='regtable'),
path('reglecturerview/', views.reglecturerview,name='reglecturerview'),
path('regattendance/', views.regattendance,name='regattendance'),
path('regstudentmark/', views.regstudentmark,name='regstudentmark'),
path('regviewresult/', views.regviewresult,name='regviewresult'),
path('reglecturer/<str:pk_profile1>/', views.reglecturer,name='reglecturer'),
path('reglectureresult/<str:pk>/', views.reglectureresult,name='reglectureresult'),
path('regstudent/<str:pk_profile>/', views.regstudent,name='regstudent'),
path('regmarks/<str:pk>/', views.regmarks,name='regmarks'),
path('regcheckmarks/<str:pk>/', views.regcheckmarks,name='regcheckmarks'),
path('regadminsturesult/<str:pk>/', views.regadminsturesult,name='regadminsturesult'),
path('regtransactions/', views.regtransactions,name='regtransactions'),
path('regsummary/<str:pk>/', views.regsummary,name='regsummary'),
path('regexamtable/', views.regexamtable,name='regexamtable'),
path('regCalendarView/', views.regCalendarView.as_view(),name='regCalendarView'),
path('regnewnotice/', views.regnewnotice,name='regnewnotice'),
path('regviewprofile/', views.regviewprofile,name='regviewprofile'),
path('regresult/', views.regresult,name='regresult'),
path('regdeletenotice/<str:pk>/', views.regdeletenotice,name='regdeletenotice'),
path('regtemplate1/', views.regtemplate1,name='regtemplate1'),
path('regtemplate2/', views.regtemplate2,name='regtemplate2'),
path('regtemplate3/', views.regtemplate3,name='regtemplate3'),
path('regtemplate4/', views.regtemplate4,name='regtemplate4'),
path('regdeletemessage/<str:pk>/', views.regdeletemessage,name='regdeletemessage'),
path('regstatus/', views.regstatus,name='regstatus'),
path('regviewstatus/', views.regviewstatus,name='regviewstatus'),
path('adminstu/', views.adminstu,name='adminstu'),
path('appadmission/<str:pk>/', views.appadmission,name='appadmission'),
path('disadmission/<str:pk>/', views.disadmission,name='disadmission'),
path('regdeletestatus/', views.regdeletestatus,name='regdeletestatus'),


path('regchangepassword/', views.regchangepassword,name='regchangepassword'),


]