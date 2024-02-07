from django.urls import path
from lecturer import views
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('lecturerdashboard/', views.lecturerdashboard,name='lecturerdashboard'),
    path('accesslogout/', LogoutView.as_view(template_name= "Permissions/accesslogout.html"),name='accesslogout'),
    
    path('lecturercalendar/', views.CalendarView.as_view(),name='lecturercalendar'),
    path('lecturercourses/', views.lecturercourses,name='lecturercourses'),
    path('lecturermessage/', views.lecturermessage,name='lecturermessage'),
    path('lecviewfaculty/', views.lecviewfaculty,name='lecviewfaculty'),
    path('studentexammarks/', views.studentexammarks,name='studentexammarks'),
    path('lecfaculty/<str:pk_profile2>/', views.lecfaculty,name='lecfaculty'),
    path('lecviewdepartment/', views.lecviewdepartment,name='lecviewdepartment'),
    path('lecdepartment/<str:pk_profile3>/', views.lecdepartment,name='lecdepartment'),
    path('lecalllecturers/', views.lecalllecturers,name='lecalllecturers'),
    path('lecallstudents/', views.lecallstudents,name='lecallstudents'),
    path('lecviewquestion/', views.lecviewquestion,name='lecviewquestion'),
    path('lecviewquestionview/<str:pk>/', views.lecviewquestionview,name='lecviewquestionview'),
    path('lectable/', views.lectable,name='lectable'),
    path('lecexamtable/', views.lecexamtable,name='lecexamtable'),
    path('lecturerprofile/', views.lecturerprofile,name='lecturerprofile'),
    path('lecattendance/', views.lecattendance,name='lecattendance'),
    path('lecresult/', views.lecresult,name='lecresult'),
    path('deletelecresult/<str:pk>/', views.deletelecresult,name='deletelecresult'),
    path('lecviewstatus/', views.lecviewstatus,name='lecviewstatus'),
    path('lecstatus/', views.lecstatus,name='lecstatus'),
    path('addexam/', views.addexam,name='addexam'),
    path('lecturernotice/', views.lecturernotice,name='lecturernotice'),
    path('lecturernewmessage/', views.lecturernewmessage,name='lecturernewmessage'),
    path('lecturerinbox/', views.lecturerinbox,name='lecturerinbox'),
    path('lecturersent/', views.lecturersent,name='lecturersent'),
    path('lecturenoticeboard/', views.lecturenoticeboard,name='lecturenoticeboard'),
    path('lecturergeneralnotice/', views.lecturergeneralnotice,name='lecturergeneralnotice'),
    path('lecturerdepartmentnotice/', views.lecturerdepartmentnotice,name='lecturerdepartmentnotice'),
    path('lecturerupdateprofile/', views.lecturerupdateprofile,name='lecturerupdateprofile'),
    path('addresult/', views.addresult,name='addresult'),
    path('stumark/<str:pk>/', views.stumark,name='stumark'),
    path('viewmark/<str:pk>/', views.viewmark,name='viewmark'),
    path('lecnotice/', views.lecnotice,name='lecnotice'),
    path('lecexamtable/', views.lecexamtable,name='lecexamtable'),
        path('lectemplate1/', views.lectemplate1,name='lectemplate1'),
        path('lectemplate2/', views.lectemplate2,name='lectemplate2'),
        path('lectemplate3/', views.lectemplate3,name='lectemplate3'),
        path('lectemplate4/', views.lectemplate4,name='lectemplate4'),
        path('lecdeletemessage/<str:pk>/', views.lecdeletemessage,name='lecdeletemessage'),
        path('lecstatus/', views.lecstatus,name='lecstatus'),
        path('lecviewstatus/', views.lecviewstatus,name='lecviewstatus'),
        path('lecdeletestatus/', views.lecdeletestatus,name='lecdeletestatus'),

    
    path('lecturerchangepassword/',views.lecturerchangepassword,name='lecturerchangepassword'),

    
    
    
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='Permissions/resetpassword.html'),name='reset_password'),
    
    path('password_reset_done/',
            auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
        
    path('password_reset_confirm/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
        
    path('reset_password_complete/', 
            auth_views.PasswordResetCompleteView.as_view(),name='reset_password_complete'),

]