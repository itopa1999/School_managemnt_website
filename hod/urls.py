from django.urls import path
from hod import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
path('hoddashboard/', views.hoddashboard,name='hoddashboard'),
path('hodviewfaculty/', views.hodviewfaculty,name='hodviewfaculty'),
path('hodfaculty/<str:pk_profile2>/', views.hodfaculty,name='hodfaculty'),
path('hodviewdepartment/', views.hodviewdepartment,name='hodviewdepartment'),
path('hoddepartment/<str:pk_profile3>/', views.hoddepartment,name='hoddepartment'),
path('hodalllecturers/', views.hodalllecturers,name='hodalllecturers'),
path('hodallstudents/', views.hodallstudents,name='hodallstudents'),
path('hodviewcourse/', views.hodviewcourse,name='hodviewcourse'),
path('hoddviewcourse/<str:pk>/', views.hoddviewcourse,name='hoddviewcourse'),
path('hodnoticeboard/', views.hodnoticeboard,name='hodnoticeboard'),
path('hodnewmessage/', views.hodnewmessage,name='hodnewmessage'),
path('hodviewmessage/', views.hodviewmessage,name='hodviewmessage'),
path('hodsentmessage/', views.hodsentmessage,name='hodsentmessage'),
path('hodtable/', views.hodtable,name='hodtable'),
path('hodlecturerview/', views.hodlecturerview,name='hodlecturerview'),
path('hodattendance/', views.hodattendance,name='hodattendance'),
path('hodstudentmark/', views.hodstudentmark,name='hodstudentmark'),
path('hodviewresult/', views.hodviewresult,name='hodviewresult'),
path('hodlecturer/<str:pk_profile1>/', views.hodlecturer,name='hodlecturer'),
path('hodlectureresult/<str:pk>/', views.hodlectureresult,name='hodlectureresult'),
path('hodstudent/<str:pk_profile>/', views.hodstudent,name='hodstudent'),
path('hodmarks/<str:pk>/', views.hodmarks,name='hodmarks'),
path('hodcheckmarks/<str:pk>/', views.hodcheckmarks,name='hodcheckmarks'),
path('hodadminsturesult/<str:pk>/', views.hodadminsturesult,name='hodadminsturesult'),
path('hodtransactions/', views.hodtransactions,name='hodtransactions'),
path('hodsummary/<str:pk>/', views.hodsummary,name='hodsummary'),
path('hodexamtable/', views.hodexamtable,name='hodexamtable'),
path('hodCalendarView/', views.hodCalendarView.as_view(),name='hodCalendarView'),
path('hodnewnotice1/', views.hodnewnotice1,name='hodnewnotice1'),
path('hodviewprofile/', views.hodviewprofile,name='hodviewprofile'),
path('hodgeneralnotice/', views.hodgeneralnotice,name='hodgeneralnotice'),
path('hoddepartmentnotice/', views.hoddepartmentnotice,name='hoddepartmentnotice'),
path('hoddeletedepnotice/<str:pk>/', views.hoddeletedepnotice,name='hoddeletedepnotice'),
path('hodexamtable/', views.hodexamtable,name='hodexamtable'),
path('hodtemplate1/', views.hodtemplate1,name='hodtemplate1'),
path('hodtemplate2/', views.hodtemplate2,name='hodtemplate2'),
path('hodtemplate3/', views.hodtemplate3,name='hodtemplate3'),
path('hodtemplate4/', views.hodtemplate4,name='hodtemplate4'),
path('hoddeletemessage/<str:pk>/', views.hoddeletemessage,name='hoddeletemessage'),
path('hodstatus/', views.hodstatus,name='hodstatus'),
path('hodviewstatus/', views.hodviewstatus,name='hodviewstatus'),
path('hoddeletestatus/', views.hoddeletestatus,name='hoddeletestatus'),
path('hodstucourse/', views.hodstucourse,name='hodstucourse'),
path('hodcoursestudent/<str:pk>/', views.hodcoursestudent,name='hodcoursestudent'),
path('hodresult/', views.hodresult,name='hodresult'),



path('hodchangepassword/', views.hodchangepassword,name='hodchangepassword'),


]