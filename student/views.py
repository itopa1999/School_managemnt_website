from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator,EmptyPage
from .decorators import *
from .forms import UserForm1,PasswordChangeForm,LibraryForm
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from administrator import models as QMODEL
from administrator import forms as QFORM
from library import models as LMODELS
from administrator import filters as QFILTER
from users.models import User
from . import models
from .models import *
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from administrator.utils import Calendar
from administrator.decorators import *


@login_required(login_url='studentlogin')
@student_only
@allow_login
def  studentchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password has been changed successfully')
            return redirect('studentchangepassword')
        else:
            messages.error(request, 'form error')
            return redirect('studentchangepassword')
    context={'form':form}
    return render(request,'student/studentchangepassword.html',context)
    



@login_required(login_url='login')
@admin_only
def registerstudent(request):
    form = UserForm1()
    if request.method =='POST':
        form = UserForm1(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        level = request.POST.get('level')
        program = request.POST.get('program')
        year = request.POST.get('year')
        if User.objects.filter(userid=userid):
            messages.info(request, "Matric_no already exists")
            return redirect('registerstudent')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerstudent')
        
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            department=QMODEL.Department.objects.get(id=request.POST.get('departmentID'))
            faculty=QMODEL.Faculty.objects.get(id=request.POST.get('facultyID'))
            group= Group.objects.get(name='student')
            user.groups.add(group)
        
            QMODEL.Student.objects.create(
                user=user,
                name=user.first_name,
                matric_no=user.userid,
                phone_no=user.phone,
                email=user.email,
                adm_year=year,
                level=level,
                program=program,
                department=department,
                faculty=faculty,
                profile_pic=user.profile_pic,
            )
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerstudent')
        else:
            messages.error(request, "form error")
            return redirect('registerstudent')
    context = {'form':form}
    return render(request, 'Permissions/registerstudent.html', context)


def is_student(user):
    return user.groups.filter(name='student').exists()



def studentlogin(request):
    if request.method == "POST":
        dep = request.POST['dep']
        userid = request.POST['userid']
        password = request.POST['password']
        user = authenticate(userid=userid, password=password)
        if user is not None:
            login(request, user)
        stu=User.objects.filter(id=request.user.id,dep=dep)
        accountapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,access=True)
        accountdisapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,access=False)
        if is_student(request.user) and accountapproval and stu:
            return redirect('studentdashboard')
        elif is_student(request.user) and accountdisapproval:
            return redirect("accesslogout")
        else:
            messages.error(request, "Invalid Credientials")
    return render(request,'student/studentlogin.html')
    
    

@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentdashboard(request):
    date=timezone.now()
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    meg= QMODEL.Message.objects.filter(student=student)[:3]
    nott= QMODEL.Notice.objects.filter(date=date)[:5]
    context={'meg':meg,'nott':nott}
    return render(request,'student/studentdashboard.html',context)



@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@library_entry
def libraryaccount(request):
    student =QMODEL.Student.objects.filter(user_id=request.user.id)
    name=student[0].name
    mat=student[0].matric_no
    dep=student[0].department
    fac=student[0].faculty
    lev=student[0].level
    pro=student[0].program
    stud=LMODELS.Student.objects.filter(name=name)
    form=LibraryForm()
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
           form=form.save(commit=False)
           form.name=name
           form.matric_no=mat
           form.department=dep
           form.faculty=fac
           form.level=lev
           form.program=pro
           stu=QMODEL.Student.objects.get(user_id=request.user.id)
           sch=QMODEL.Schoollevy.objects.get(name__startswith='lib')
           tra=QMODEL.Transaction.objects.filter(student=stu,schoollevy=sch)
           myFilter=QFILTER.DebitFilter(request.GET, queryset=tra)
           tra=myFilter.qs
           total_paid=tra.aggregate(Sum('debit'))['debit__sum']
           total_credit=tra.aggregate(Sum('credit'))['credit__sum']
           if total_paid is None:
                total_paid=0
           else:
                total_paid
           if total_credit is None:
                total_credit=0
           else:
                total_credit
           bal=total_credit-total_paid
           print(bal)
           if bal > 0:
                messages.info(request, 'you cannot be added, you havent balance  your library fee')
                return redirect('libraryaccount')
           elif stud:
                messages.error(request, 'You are already added to library')
                return redirect('libraryaccount')
           else:
                form.save()
                messages.success(request, 'you are addded successfully')
                return redirect('libraryaccount') 
    context={'form':form}
    return render(request,'student/libraryaccount.html',context)




@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@library_entry
def studentviewissuedbook(request):
    stu1 =QMODEL.Student.objects.get(user_id=request.user.id)
    student2=LMODELS.Student.objects.get(name=stu1)
    if not student2:
        messages.info(request, "you haven't been added to librarian list yet.")
        return redirect('libraryaccount')
    
    issuedbooks=LMODELS.IssuedBook.objects.filter(student=student2)
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(LMODELS.Book.objects.filter(isbn=ib.isbn))
        students=list(LMODELS.Student.objects.filter(department=ib.department))
        i=0
        for l in books:
            t=(students[i].name,students[i].department,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)
    messages.info(request, 'Fine will be Issued to You after 15days of issued books')
    context={'li':li}
    return render(request,'student/studentviewissuedbook.html',context)


@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@library_entry
def studentviewbook(request):
    stu1 =QMODEL.Student.objects.get(user_id=request.user.id)
    student2=LMODELS.Student.objects.filter(name=stu1)
    if not student2:
        messages.info(request, "you haven't been added to librarian list yet.")
        return redirect('libraryaccount')
    stu =QMODEL.Student.objects.filter(user_id=request.user.id)
    name=stu[0].name
    student1=LMODELS.Student.objects.filter(name=name)
    dep=student1[0].department
    books=LMODELS.Book.objects.filter(department=1)
    context={'books':books}
    return render(request,'student/studentviewbook.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def examtable(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
    hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
    student =QMODEL.Course.objects.all() 
    if ndstudent:
        tim=QMODEL.Exam_Timetable.objects.filter(week="Monday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim1=QMODEL.Exam_Timetable.objects.filter(week="Tuesday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim2=QMODEL.Exam_Timetable.objects.filter(week="Wednesday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim3=QMODEL.Exam_Timetable.objects.filter(week="Thursday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim4=QMODEL.Exam_Timetable.objects.filter(week="Friday",department=dep,course__semester__startswith="ND").order_by('timefrom')
    elif hndstudent:
        tim=QMODEL.Exam_Timetable.objects.filter(week="Monday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim1=QMODEL.Exam_Timetable.objects.filter(week="Tuesday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim2=QMODEL.Exam_Timetable.objects.filter(week="Wednesday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim3=QMODEL.Exam_Timetable.objects.filter(week="Thursday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim4=QMODEL.Exam_Timetable.objects.filter(week="Friday",department=dep,course__semester__startswith="HND").order_by('timefrom')
    else:
        messages.info(request, 'This form must be filled before accessing some features')
        return redirect('viewprofile')
        
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'student/examtable.html',context)
 
 
@login_required(login_url='studentlogin')
@student_only
@allow_login
def timetable(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
    hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
    student =QMODEL.Course.objects.all() 
    if ndstudent:
        tim=QMODEL.Timetable.objects.filter(week="Monday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim1=QMODEL.Timetable.objects.filter(week="Tuesday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim2=QMODEL.Timetable.objects.filter(week="Wednesday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim3=QMODEL.Timetable.objects.filter(week="Thursday",department=dep,course__semester__startswith="ND").order_by('timefrom')
        tim4=QMODEL.Timetable.objects.filter(week="Friday",department=dep,course__semester__startswith="ND").order_by('timefrom')
    elif hndstudent:
        tim=QMODEL.Timetable.objects.filter(week="Monday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim1=QMODEL.Timetable.objects.filter(week="Tuesday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim2=QMODEL.Timetable.objects.filter(week="Wednesday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim3=QMODEL.Timetable.objects.filter(week="Thursday",department=dep,course__semester__startswith="HND").order_by('timefrom')
        tim4=QMODEL.Timetable.objects.filter(week="Friday",department=dep,course__semester__startswith="HND").order_by('timefrom')
    else:
        messages.info(request, 'This form must be filled before accessing some features')
        return redirect('viewprofile')
        
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'student/timetable.html',context)


 
@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@allow_exam
@exam_entry
def studentexam(request):
    stu1=QMODEL.Student.objects.get(user_id=request.user.id)
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    lev=stu[0].level
    mat=stu[0].matric_no
    ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
    hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
    if ndstudent:
        courses=QMODEL.Register_course.objects.filter(semester__startswith="ND")
    elif hndstudent:
        courses=QMODEL.Register_course.objects.filter(semester__startswith="HND")
    else:
        messages.info(request, 'This form must be filled before accessing some features')
        return redirect('viewprofile')
    if not courses:
        messages.info(request, "You Haven't Registered Any Course Yet, Please Visit Any Of The Admin For Course Registration.")
        return redirect('studentdashboard')
    if request.method == "POST":
        courses = request.POST['courses']
        try:
            course=QMODEL.Course.objects.get(name=courses)
        except ObjectDoesNotExist:
            messages.error(request, "you havent choosen any valid course")
            return redirect('studentexam')
        total_questions=QMODEL.Question.objects.all().filter(course=course).count()
        questions=QMODEL.Question.objects.all().filter(course=course)
        total_marks=0
        for q in questions:
            total_marks=total_marks + q.marks
        if total_marks==0:
            messages.info(request, "There is no question in this Exam yet")
            return redirect('studentexam')
        else:
            context={'course':course,'total_questions':total_questions,
                'total_marks':total_marks,'stu1':stu1,'dep':dep,'lev':lev,'mat':mat}
            return render(request,'student/takeexam.html',context)
            
    context={'courses':courses,}
    return render(request,'student/studentexam.html',context)
    
    
    


@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentmessage(request):
    return render(request,'student/studentmessage.html')


@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentinbox(request):
    user=Group.objects.get(name="student")
    student=QMODEL.Student.objects.get(user_id=request.user.id)
    meg= QMODEL.Message.objects.filter(student=student)
    meg1= QMODEL.Message.objects.filter(group=user)
    context={'meg':meg,'meg1':meg1}
    return render(request,'student/studentinbox.html',context)


@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentsent(request):
    student=QMODEL.Student.objects.get(user_id=request.user.id)
    meg=QMODEL.Message.objects.filter(sender=student)
    context={'meg':meg}
    return render(request,'student/studentsent.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentnewmessage(request):
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    student1 =QMODEL.Student.objects.filter(user_id=request.user.id)
    pic=student1[0].profile_pic
    form= QFORM.MessageForm()
    if request.method == 'POST':
        form =  QFORM.MessageForm(request.POST, request.FILES)
        if form.is_valid():
           form=form.save(commit=False)
           lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
           group=Group.objects.get(id=request.POST.get('groupID'))
           form.lecturer=lecturer
           form.group=group
           form.sender=student
           form.profile_pic=pic
           form.save()
           messages.success(request, 'message sent successfully')
           return redirect('studentnewmessage')
        else:
           messages.error(request, 'error')
           return redirect('studentnewmessage')
    context={'form':form}
    return render(request,'student/studentnewmessage.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def viewcourses(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
    hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
    if ndstudent:
        cou=QMODEL.Register_course.objects.filter(semester="ND1 first Semester")
        cou1=QMODEL.Register_course.objects.filter(semester="ND1 second Semester")
        cou2=QMODEL.Register_course.objects.filter(semester="ND2 first Semester")
        cou3=QMODEL.Register_course.objects.filter(semester="ND2 second Semester")
        tit="ND1 FIRST SEMESTER"
        tit1="ND1 SECOND SEMESTER"
        tit2="ND2 FIRST SEMESTER"
        tit3="ND2 SECOND SEMESTER"
        total=cou.aggregate(Sum('course_unit'))['course_unit__sum']
        total1=cou1.aggregate(Sum('course_unit'))['course_unit__sum']
        total2=cou2.aggregate(Sum('course_unit'))['course_unit__sum']
        total3=cou3.aggregate(Sum('course_unit'))['course_unit__sum']
    elif hndstudent:
        cou=QMODEL.Register_course.objects.filter(semester="HND1 first Semester")
        cou1=QMODEL.Register_course.objects.filter(semester="HND1 second Semester")
        cou2=QMODEL.Register_course.objects.filter(semester="HND2 first Semester")
        cou3=QMODEL.Register_course.objects.filter(semester="HND2 second Semester")
        tit="HND1 FIRST SEMESTER"
        tit1="HND1 SECOND SEMESTER"
        tit2="HND2 FIRST SEMESTER"
        tit3="HND2 SECOND SEMESTER"
        total=cou.aggregate(Sum('course_unit'))['course_unit__sum']
        total1=cou1.aggregate(Sum('course_unit'))['course_unit__sum']
        total2=cou2.aggregate(Sum('course_unit'))['course_unit__sum']
        total3=cou3.aggregate(Sum('course_unit'))['course_unit__sum']
    else:
        messages.info(request, 'You havent Registered any course yet')
        return redirect('stucourse')
    context={'cou':cou,'cou1':cou1,'cou2':cou2,'cou3':cou3,
             'tit':tit,'tit1':tit1,'tit2':tit2,'tit3':tit3,'stu':stu,
             'total':total,'total1':total1,'total2':total2,
             'total3':total3}
    return render(request,'student/viewcourses.html',context)


@login_required(login_url='studentlogin')
@student_only
@allow_login
def payment(request):
    sch=QMODEL.Schoollevy.objects.all()
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    context={'sch':sch}
    if request.method == "POST":
        levies= request.POST['levies']
        try:
            sch=QMODEL.Schoollevy.objects.get(name=levies)
        except ObjectDoesNotExist:
            messages.error(request, "you havent choosen any valid Levy to view Transactions")
            return redirect('payment')
        tra=QMODEL.Transaction.objects.filter(schoollevy=sch,student=student)
        total_paid=tra.aggregate(Sum('debit'))['debit__sum']
        total_credit=tra.aggregate(Sum('credit'))['credit__sum']
        if total_paid is None and total_credit is None:
            messages.info(request,'There is no transaction')
            return redirect('payment')
        if total_paid is None:
            total_paid=0
        else:
            total_paid
        if total_credit is None:
            total_credit=0
        else:
            total_credit
        bal=total_credit-total_paid
        
        mydict={
            'tra':tra,
            'total_paid':total_paid,
            'total_credit':total_credit,'bal':bal,
        }
        return render(request,'student/viewpayment.html',context=mydict)
        
    
    return render(request,'student/payment.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def  viewpayment(request):
    context={}
    return render(request,'student/viewpayment.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def stustatus(request):
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    student1 =QMODEL.Student.objects.filter(user_id=request.user.id)
    pic=student1[0].profile_pic
    form=QFORM.StatusForm()
    if request.method=='POST':
        user2=request.POST.get('user')
        form=QFORM.StatusForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.profile_pic=pic
            form.user=student
            if QMODEL.Status.objects.filter(user=form.user):
                messages.info(request, 'You can only upload once, you can delete previous status for new one.')
                return redirect('stustatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('stustatus')
        else:
            messages.error(request, 'form error')
            return redirect('status')
    context={'form':form}
    return render(request,'student/stustatus.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def  studeletestatus(request):
    user=QMODEL.Student.objects.get(user_id=request.user.id)
    sta=QMODEL.Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('stuviewstatus')


@login_required(login_url='studentlogin')
@student_only
@allow_login
def  stuviewstatus(request):
    sta=QMODEL.Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'student/stuviewstatus.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def viewprofile(request):
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    stu=QMODEL.Student.objects.filter(name=student)
    form = QFORM.StudentForm1(instance=student)
    if request.method =='POST':
        form = QFORM.StudentForm1(request.POST, request.FILES,instance=student)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('viewprofile')
        else:
            messages.error(request, "form error")
            return redirect('viewprofile')
    context = {'form':form,'stu':stu}
    return render(request,'student/viewprofile.html',context)


@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@allow_exam
@exam_entry
def startexam(request,pk):
    student =QMODEL.Student.objects.get(user_id=request.user.id)
    course=QMODEL.Course.objects.get(id=pk)
    res=QMODEL.Result1.objects.filter(course=course,student=student)
    if res:
        messages.info(request, "You have attended this Exam")
        return redirect('studentexam')
    else:
        course=QMODEL.Course.objects.get(id=pk)
        questions=QMODEL.Question.objects.all().filter(course=course)
        if request.method=='POST':
            pass
        context={'course':course,'questions':questions}
        response= render(request,'student/startexam.html',context)
        response.set_cookie('course_id',course.id)
        return response


@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@allow_exam
@exam_entry
def calculatemarks(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        total_marks=0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i in range(len(questions)):
            
            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        student = QMODEL.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result1()
        result.marks=total_marks
        result.course=course
        result.student=student
        result.save()
        messages.success(request, 'Your exam has been submitted successfully and your result is ready')
        return redirect('studentmarks')

@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@allow_exam
@exam_entry
def score(request):
    context={}
    return render(request,'student/score.html',context)



@login_required(login_url='studentlogin')
@admissionstatus
@student_only
@allow_login
@allow_exam
@exam_entry
def studentmarks(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
    hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
    if ndstudent:
        courses=QMODEL.Register_course.objects.filter(semester__startswith="ND")
    elif hndstudent:
        courses=QMODEL.Register_course.objects.filter(semester__startswith="HND")
    else:
        messages.info(request, 'This form must be filled before accessing some features')
        return redirect('viewprofile')
    if not courses:
        messages.info(request, "You Haven't Registered Any Course Yet, Please Visit Any Of The Admin For Course Registration.")
        return redirect('studentdashboard')
    if request.method == "POST":
        cou = request.POST['cou']
        try:
            course=QMODEL.Course.objects.get(name=cou)
        except ObjectDoesNotExist:
            messages.info(request, "you havent choosen any valid course")
            return redirect('studentmarks')
        questions=QMODEL.Question.objects.all().filter(course=course)
        total_marks=0
        for q in questions:
            total_marks=total_marks + q.marks
        student =QMODEL.Student.objects.get(user_id=request.user.id)
        result= QMODEL.Result1.objects.filter(course=course,student=student)
        if not result:
            messages.info(request, "You haven't attended this Exam")
            return redirect('studentexam')
        if result:
            results= QMODEL.Result1.objects.filter(course=course,student=student)
            context={'results':results,'total_marks':total_marks,'questions':questions}
            return render(request,'student/score.html',context)   
    context={'courses':courses}
    return render(request,'student/studentmarks.html',context)




@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentnoticeboard(request):
    return render(request,'student/studentnoticeboard.html')


@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentgeneralnotice(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].adm_year
    notice=QMODEL.Notice.objects.filter(year=dep)
    context={'notice':notice}
    return render(request,'student/studentgeneralnotice.html',context)



@login_required(login_url='studentlogin')
@student_only
@allow_login
def studentdepartmentnotice(request):
    stu=QMODEL.Student.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    dep1=stu[0].adm_year
    dep2=stu[0].level
    notice=QMODEL.DepartmentNotice.objects.filter(department=dep,year=dep1,level=dep2)
    context={'notice':notice}
    return render(request,'student/studentdepartmentnotice.html',context)


@login_required(login_url='studentlogin')
@student_only
@allow_login
def adminstatus(request):
    user=User.objects.filter(id=request.user.id)
    token=user[0].token
    token=user[0].token
    if request.method=='POST':
        token1=request.POST['token']
        if token != token1:
            messages.error(request, 'Invalid token submitted')
            return redirect('adminstatus')
        else:
            stu=QMODEL.Student.objects.get(user_id=request.user.id)
            sch=QMODEL.Schoollevy.objects.get(name__startswith='acce')
            tra=QMODEL.Transaction.objects.filter(student=stu,schoollevy=sch)
            myFilter=QFILTER.DebitFilter(request.GET, queryset=tra)
            tra=myFilter.qs
            total_paid=tra.aggregate(Sum('debit'))['debit__sum']
            total_credit=tra.aggregate(Sum('credit'))['credit__sum']
            if total_paid is None:
                total_paid=0
            else:
                total_paid
            if total_credit is None:
                total_credit=0
            else:
                total_credit
            bal=total_credit-total_paid
            print(bal)
            if bal > 0:
                messages.info(request, 'You cannot view this page, you havent pay Admission fee')
                return redirect('adminstatus')
            accountapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,adminstatus=True)
            if accountapproval:
                info=('Your Admission has been granted.')
            else:
                messages.info(request, 'Your Admission has not been granted yet, check sometime later.')
                return redirect('adminstatus')
            context={'info':info,'user':user}
            return render(request,'student/adminstatus1.html',context)
    context={}
    return render(request,'student/adminstatus.html',context)


class CalendarView(generic.ListView):
    model = QMODEL.Event
    template_name = 'student/studentcalendar.html'
 
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
 
         # use today's date for the calendar
         d = get_date(self.request.GET.get('day', None))
 
         # Instantiate our calendar class with today's year and date
         cal = Calendar(d.year, d.month)
 
         # Call the formatmonth method, which returns our calendar as a table
         html_cal = cal.formatmonth(withyear=True)
         context['calendar'] = mark_safe(html_cal)
         return context
 
def get_date(req_day):
     if req_day:
         year, month = (int(x) for x in req_day.split('-'))
         return date(year, month, day=1)
     return datetime.today()