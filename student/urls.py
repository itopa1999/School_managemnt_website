from django.urls import path
from student import views
from student import result
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [
path('studentlogin/', views.studentlogin,name='studentlogin'),
path('studentlogout/', LogoutView.as_view(template_name= "student/studentlogout.html"),name='studentlogout'),
path('accesslogout/', LogoutView.as_view(template_name= "Permissions/accesslogout.html"),name='accesslogout'),
path('accesslogout1/', LogoutView.as_view(template_name= "Permissions/accesslogout1.html"),name='accesslogout1'),
path('registerstudent/', views.registerstudent, name="registerstudent"),


path('studentdashboard/', views.studentdashboard,name='studentdashboard'),
path('libraryaccount/', views.libraryaccount,name='libraryaccount'),
path('studentviewbook/', views.studentviewbook,name='studentviewbook'),
path('studentviewissuedbook/', views.studentviewissuedbook,name='studentviewissuedbook'),
path('viewcourses/', views.viewcourses,name='viewcourses'),
path('examtable/', views.examtable,name='examtable'),
path('timetable/', views.timetable,name='timetable'),

path('sturesult/', result.sturesult,name='sturesult'),
path('studentmessage/', views.studentmessage,name='studentmessage'),
path('studentinbox/', views.studentinbox,name='studentinbox'),
path('studentsent/', views.studentsent,name='studentsent'),
path('studentnewmessage/', views.studentnewmessage,name='studentnewmessage'),
path('studentcalendar/', views.CalendarView.as_view(),name='studentcalendar'),
path('stustatus/', views.stustatus,name='stustatus'),
path('studentnoticeboard/', views.studentnoticeboard,name='studentnoticeboard'),
path('studentgeneralnotice/', views.studentgeneralnotice,name='studentgeneralnotice'),
path('studentdepartmentnotice/', views.studentdepartmentnotice,name='studentdepartmentnotice'),
path('payment/', views.payment,name='payment'),
path('viewpayment/', views.viewpayment,name='viewpayment'),

path('studentexam/', views.studentexam,name='studentexam'),
path('viewprofile/', views.viewprofile,name='viewprofile'),
path('startexam/<str:pk>/', views.startexam,name='startexam'),

path('calculatemarks/', views.calculatemarks,name='calculatemarks'),
path('score/', views.score,name='score'),
path('studentmarks/', views.studentmarks,name='studentmarks'),
path('stuviewstatus/', views.stuviewstatus,name='stuviewstatus'),
path('adminstatus/', views.adminstatus,name='adminstatus'),
path('studeletestatus/', views.studeletestatus,name='studeletestatus'),



path('studentchangepassword/',views.studentchangepassword,name='studentchangepassword'),
    
    
   
]