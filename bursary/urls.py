from django.urls import path
from bursary import views
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView


urlpatterns = [
path('bursarydashboard/', views.bursarydashboard,name='bursarydashboard'),
path('burviewfaculty/', views.burviewfaculty,name='burviewfaculty'),
path('burfaculty/<str:pk_profile2>/', views.burfaculty,name='burfaculty'),
path('burviewdepartment/', views.burviewdepartment,name='burviewdepartment'),
path('burdepartment/<str:pk_profile3>/', views.burdepartment,name='burdepartment'),
path('buralllecturers/', views.buralllecturers,name='buralllecturers'),
path('burallstudents/', views.burallstudents,name='burallstudents'),
path('burviewcourse/', views.burviewcourse,name='burviewcourse'),
path('bureviewcourse/<str:pk>/', views.bureviewcourse,name='bureviewcourse'),
path('burnoticeboard/', views.burnoticeboard,name='burnoticeboard'),
path('burnewmessage/', views.burnewmessage,name='burnewmessage'),
path('burviewmessage/', views.burviewmessage,name='burviewmessage'),
path('bursentmessage/', views.bursentmessage,name='bursentmessage'),
path('burtable/', views.burtable,name='burtable'),
path('burlecturerview/', views.burlecturerview,name='burlecturerview'),
path('burattendance/', views.burattendance,name='burattendance'),
path('burstudentmark/', views.burstudentmark,name='burstudentmark'),
path('burviewresult/', views.burviewresult,name='burviewresult'),
path('burlecturer/<str:pk_profile1>/', views.burlecturer,name='burlecturer'),
path('burlectureresult/<str:pk>/', views.burlectureresult,name='burlectureresult'),
path('burstudent/<str:pk_profile>/', views.burstudent,name='burstudent'),
path('burmarks/<str:pk>/', views.burmarks,name='burmarks'),
path('burcheckmarks/<str:pk>/', views.burcheckmarks,name='burcheckmarks'),
path('buradminsturesult/<str:pk>/', views.buradminsturesult,name='buradminsturesult'),
path('burtransactions/', views.burtransactions,name='burtransactions'),
path('burdebitpayment/', views.burdebitpayment,name='burdebitpayment'),
path('burcreditpayment/', views.burcreditpayment,name='burcreditpayment'),
path('bursummary/<str:pk>/', views.bursummary,name='bursummary'),
path('burreceipt/<str:pk>/', views.burreceipt,name='burreceipt'),
path('burexamtable/', views.burexamtable,name='burexamtable'),
path('burtemplate1/', views.burtemplate1,name='burtemplate1'),
path('burtemplate2/', views.burtemplate2,name='burtemplate2'),
path('burtemplate3/', views.burtemplate3,name='burtemplate3'),
path('burtemplate4/', views.burtemplate4,name='burtemplate4'),
path('burdeletemessage/<str:pk>/', views.burdeletemessage,name='burdeletemessage'),
path('burstatus/', views.burstatus,name='burstatus'),
path('burviewstatus/', views.burviewstatus,name='burviewstatus'),
path('burdeletestatus/', views.burdeletestatus,name='burdeletestatus'),
path('burviewprofile/', views.burviewprofile,name='burviewprofile'),
path('burCalendarView/', views.burCalendarView.as_view(),name='burCalendarView'),





path('burchangepassword/', views.burchangepassword,name='burchangepassword'),


]