from django.shortcuts import render,reverse,redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.decorators import login_required,user_passes_test
from .decorators import *
from .forms import *
from administrator.models import *
from administrator.forms import  *
from student.models import *
from . import models
from users.models import User
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from administrator.utils import Calendar
from administrator.decorators import *

# Create your views here.
@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecturerchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('lecturersetting')
    context={'form':form}
    return render(request,'lecturer/lecturerchangepassword.html',context)




@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturerdashboard(request):
    return render(request,'lecturer/lecturerdashboard.html')


@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturercourses(request):
    lecturer =Lecturer.objects.get(user_id=request.user.id)
    cou=Course.objects.filter(lecturer=lecturer)
    context={'cou':cou}
    return render(request,'lecturer/lecturercourses.html',context)




@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturermessage(request):
    return render(request,'lecturer/lecturermessage.html')





@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturernewmessage(request):
    form= MessageForm()
    
    context={'form':form}
    return render(request,'lecturer/lecturernewmessage.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturerinbox(request):
    user=Group.objects.get(name="lecturer")
    meg1= Message.objects.filter(group=user)
    context={'meg':meg}
    return render(request,'lecturer/lecturerinbox.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturersent(request):
    lecturer=Lecturer.objects.get(user_id=request.user.id)
    meg=Message.objects.filter(sender=lecturer)
    context={'meg':meg}
    return render(request,'lecturer/lecturersent.html',context)

@login_required(login_url='login')
@lecturer_only
@allow_user
def lecviewfaculty(request):
    fac=Faculty.objects.all()
    context = {'fac':fac}
    return render(request,'lecturer/lecviewfaculty.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecfaculty(request, pk_profile2):
    fac=Faculty.objects.get(id=pk_profile2)
    dep=Department.objects.filter(faculty=pk_profile2)
    depcount=dep.count()
    stucount=Student.objects.filter(faculty=pk_profile2).count()
    stucount1=Student.objects.filter(faculty=pk_profile2)
    nd=stucount1.filter(level='ND').count()
    hnd=stucount1.filter(level='HND').count()
    pt= stucount1.filter(program='Part time').count()
    ft= stucount1.filter(program='Full time').count()
    context = {'fac':fac, 'dep':dep, 'depcount':depcount, 
              'stucount':stucount,'item':fac,'pt':pt,
             'nd':nd,'hnd':hnd,'ft':ft}
    return render(request, 'lecturer/lecfaculty.html', context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecviewdepartment(request):
    dep=Department.objects.all()
    context = {'dep':dep}
    return render(request,'lecturer/lecviewdepartment.html',context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecdepartment(request, pk_profile3):
    dep=Department.objects.get(id=pk_profile3)
    depu = Department.objects.get(id=pk_profile3)
    countstu=Student.objects.filter(department=pk_profile3).count()
    stu=Student.objects.filter(department=pk_profile3)
    hnd= stu.filter(level='HND').count()
    nd= stu.filter(level='ND').count()
    pt= stu.filter(program='Part time').count()
    ft= stu.filter(program='Full time').count()
    context= {'dep':dep,'item':dep,'depu':depu,
              'countstu':countstu,'hnd':hnd,'nd':nd,'pt':pt,
              'ft':ft}
    return render(request, 'lecturer/lecdepartment.html', context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecalllecturers(request):
    lec= Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'lecturer/lecalllecturers.html',context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecallstudents(request):
    stu= Student.objects.all().order_by('adm_year')
    context={'stu':stu}
    return render(request,'lecturer/lecallstudents.html',context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturerupdateprofile(request):
    lecturer=request.user.lecturer
    form=StaffForm(instance=lecturer)
    if request.method =='POST':
        form=StaffForm(request.POST, request.FILES,instance=lecturer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated successfully')
            return redirect('lecturersetting')
    context={'form':form}
    return render(request,'lecturer/lecturerupdateprofile.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecturerprofile(request):
    lec=Lecturer.objects.get(user_id=request.user.id)
    lec1=Lecturer.objects.filter(name=lec)
    form = LecturerForm2(instance=lec)
    if request.method =='POST':
        form = LecturerForm2(request.POST, request.FILES,instance=lec)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('lecturerprofile')
        else:
            messages.error(request, "form error")
            return redirect('lecturerprofile')
    context = {'form':form,'lec1':lec1}
    return render(request,'lecturer/lecturerprofile.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def studentexammarks(request):
    lec=Lecturer.objects.filter(user_id=request.user.id)
    dep=lec[0].department
    stu= Student.objects.filter(department=dep)
    context={'stu':stu}
    return render(request,'lecturer/studentexammarks.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
@exam_entry
def addexam(request):
    lec=Lecturer.objects.get(user_id=request.user.id)
    questionForm=QuestionForm()
    if request.method=='POST':
        questionForm=QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.user=lec
            question.save()
            messages.success(request, 'Question has been submitted')
            return redirect('addexam')
        else:
            print("form is invalid")
        return redirect('addexam')
    context={'questionForm':questionForm}
    return render(request,'lecturer/addexam.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
@exam_entry
def  lecviewquestion(request):
    lec=Lecturer.objects.get(user_id=request.user.id)
    cou =Course.objects.filter(lecturer=lec)
    context={'cou':cou}
    return render(request,'lecturer/lecviewquestion.html',{'cou':cou})



@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecviewquestionview(request,pk):
    course=Course.objects.get(id=pk)
    que=Question.objects.filter(course=course)
    if not que:
        messages.error(request, 'There is no Question for this Course yet!!!!!')
        return redirect('viewquestion')
    p=Paginator(que, 1)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
            page = p.page(1)
    context={'que':page}
    return render(request,'lecturer/lecviewquestionview.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def addresult(request):
    lec =Lecturer.objects.get(user_id=request.user.id)
    print(lec)
    form = StudentResultForm()
    if request.method == 'POST':
       form = StudentResultForm(request.POST)
       if form.is_valid():
           form=form.save(commit=False)
           course=Course.objects.get(id=request.POST.get('courseID'))
           cou=Course.objects.filter(name=course)
           cu=cou[0].course_unit
           student=Student.objects.get(id=request.POST.get('studentID'))
           form.student=student
           form.course=course
           form.lecturer=lec
           form.cu=cu
           form.save()
           messages.success(request, "Result has been submitted Successfully to the admin")
           return redirect('addresult')
    context = {'form':form}
    return render(request,'lecturer/addresult.html',context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def stumark(request,pk):
    lec=Lecturer.objects.get(user_id=request.user.id)
    cou =Course.objects.filter(lecturer=lec)
    context={'cou':cou}
    response =  render(request,'lecturer/stumark.html',context)
    response.set_cookie('student_id',str(pk))
    return response



@login_required(login_url='login')
@lecturer_only
@allow_user
def viewmark(request,pk):
    course =Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    student_id = request.COOKIES.get('student_id')
    student= Student.objects.get(id=student_id)
    result= Result1.objects.all().filter(course=course).filter(student=student)
    if result:
        res= Result1.objects.all().filter(course=course).filter(student=student)
    else:
        messages.error(request, "Student haven't attended this Exam")
        return redirect('studentexammarks')
    context={'res':res,'total_marks':total_marks}
    return render(request,'lecturer/viewmark.html',context)




@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturernotice(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form=DepartmentNoticeForm()
    if request.method=='POST':
        form=DepartmentNoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.department=department
            form.profile_pic=pic
            form.sender=user
            form.save()
            messages.success(request, 'Notice has been pasted to noticeboard')
            return redirect('lecturernotice')
        else:
            messages.error(request, 'form error')
            return redirect('lecturernotice')
    context={'form':form}
    return render(request,'lecturer/lecturernotice.html',context)



login_required(login_url='lecturerlogin')

def lecattendance(request):
    user1 =Lecturer.objects.filter(user_id=request.user.id,attaccess=False)
    if user1:
        messages.error(request, "you don't have access to view this page")
        return redirect('lecturerdashboard')
    user =User.objects.filter(id=request.user.id)
    stu=Lecturer.objects.filter(user_id=request.user.id)
    name=user[0].first_name
    dep=stu[0].department
    form=AttendanceForm()
    if request.method=='POST':
        form=AttendanceForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.course=course
            form.department=department
            form.lecturer=name
            form.save()
            messages.success(request, 'Attendance submitted successfully')
            return redirect('lecattendance')
        else:
            messages.error(request, 'Form error')
            return redirect('lecattendance')
    context={'form':form}
    return render(request,'lecturer/lecattendance.html',context)



login_required(login_url='lecturerlogin')

def lecresult(request):
    user =Lecturer.objects.get(user_id=request.user.id)
    res=LecturerResult.objects.filter(lecturer=user).order_by('date')
    context={'res':res}
    return render(request,'lecturer/lecresult.html',context)


def deletelecresult(request, pk):
   res=LecturerResult.objects.get(id=pk)
   res.delete()
   messages.success(request, 'Result has been deleted successfully')
   return redirect('lecresult')
 





login_required(login_url='lecturerlogin')

def lecturenoticeboard(request):
    
    return render(request,'lecturer/lecturenoticeboard.html')


@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturergeneralnotice(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'lecturer/lecturergeneralnotice.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecnotice(request):
    return render(request,'lecturer/lecnotice.html')



@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturerdepartmentnotice(request):
    stu=Lecturer.objects.filter(user_id=request.user.id)
    dep=stu[0].department
    notice=DepartmentNotice.objects.filter(department=dep)
    context={'notice':notice}
    return render(request,'lecturer/lecturerdepartmentnotice.html',context)



@login_required(login_url='login')
@lecturer_only
@allow_user
def lectable(request):
    return render(request,'lecturer/lectable.html')



@login_required(login_url='login')
@lecturer_only
@allow_user
def lecexamtable(request):
    return render(request,'lecturer/lecexamtable.html')



@login_required(login_url='login')
@lecturer_only
@allow_user
def lecturerdashboard(request):
    date=timezone.now()
    user1=Group.objects.get(name='admin')
    meg= Message.objects.filter(group=user1)[:3]
    nott= Notice.objects.filter(date=date)[:5]
    stu= Student.objects.all()
    lec= Lecturer.objects.all()
    lecount= lec.count()
    fac=Faculty.objects.count()
    dept=Department.objects.count()
    facu=Faculty.objects.all()
    dep=Department.objects.all()
    total_students = stu.count()
    ma1= stu.filter(sex='Male').count()
    fe1= stu.filter(sex='Female').count()
    hnd= stu.filter(level='HND').count()
    nd= stu.filter(level='ND').count()
    pt =stu.filter(program='Part time').count()
    ft= stu.filter(program='Full time').count()
    hndpt=stu.filter(level='HND',program='Part time').count()
    hndft=stu.filter(level='HND',program='Full time').count()
    ndpt=stu.filter(level='ND',program='Part time').count()
    ndft=stu.filter(level='ND',program='Full time').count()
    name=['HND','ND','PART-TIME','FULL-TIME']
    num=[hnd,nd,pt,ft]
    ma=['MALE','FEMALE']
    fe=[ma1,fe1]
    status=Status.objects.all()[0:3]
    context={'stu':stu,'total_students':total_students,'fac':fac, 'dept':dept,
             'hnd':hnd, 'nd':nd, 'pt':pt, 'ft':ft,'name':name,'num':num,
             'facu':facu, 'dep':dep,'hndpt':hndpt,'hndft':hndft,'ndpt':ndpt,
             'ndft':ndft,'lec':lec,'lecount':lecount,'status':status,
             'meg':meg,'nott':nott,'ma':ma,'fe':fe}
    return render(request,'lecturer/lecturerdashboard.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lectemplate1(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form= MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
           form=form.save(commit=False)
           lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
           group=Group.objects.get(id=request.POST.get('groupID'))
           student=Student.objects.get(id=request.POST.get('studentID'))
           form.lecturer=lecturer
           form.group=group
           form.student=student
           form.sender=user
           form.profile_pic=pic
           form.save()
           messages.success(request, 'message sent successfully')
           return redirect('lectemplate1') 
        else:
            messages.error(request, 'Message error')
            return redirect('lectemplate1') 
    context={'form':form}
    return render(request, 'lecturer/lectemplate1.html', context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lectemplate2(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form= MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
           form=form.save(commit=False)
           lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
           group=Group.objects.get(id=request.POST.get('groupID'))
           form.lecturer=lecturer
           form.group=group
           form.sender=user
           form.profile_pic=pic
           form.save()
           messages.success(request, 'message sent successfully')
           return redirect('lectemplate2') 
        else:
            messages.error(request, 'Message error')
            return redirect('lectemplate2') 
    context={'form':form}
    return render(request, 'lecturer/lectemplate2.html', context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lectemplate3(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form= MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
           form=form.save(commit=False)
           group=Group.objects.get(id=request.POST.get('groupID'))
           student=Student.objects.get(id=request.POST.get('studentID'))
           form.group=group
           form.student=student
           form.sender=user
           form.profile_pic=pic
           form.save()
           messages.success(request, 'message sent successfully')
           return redirect('lectemplate3') 
        else:
            messages.error(request, 'Message error')
            return redirect('lectemplate3') 
    context={'form':form}
    return render(request, 'lecturer/lectemplate3.html', context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lectemplate4(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form= MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
           form=form.save(commit=False)
           lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
           student=Student.objects.get(id=request.POST.get('studentID'))
           form.lecturer=lecturer
           form.student=student
           form.sender=user
           form.profile_pic=pic
           form.save()
           messages.success(request, 'message sent successfully')
           return redirect('lectemplate4') 
        else:
            messages.error(request, 'Message error')
            return redirect('lectemplate4') 
    context={'form':form}
    return render(request, 'lecturer/lectemplate4.html', context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('lecsentmessage')


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'lecturer/lecexamtable.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lectable(request):
    tim=Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'lecturer/lectable.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecstatus(request):
    user=User.objects.get(id=request.user.id)
    user1=User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    form=StatusForm()
    if request.method=='POST':
        user2=request.POST.get('user')
        form=StatusForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.profile_pic=pic
            form.user=user
            if Status.objects.filter(user=form.user):
                messages.info(request, 'You can only upload once, you can delete previous status for new one.')
                return redirect('lecstatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('lecstatus')
        else:
            messages.error(request, 'form error')
            return redirect('lecstatus')
    context={'form':form}
    return render(request,'lecturer/lecstatus.html',context)


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecdeletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('lecviewstatus')


@login_required(login_url='login')
@lecturer_only
@allow_user
def  lecviewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'lecturer/lecviewstatus.html',context)

    
    
class CalendarView(generic.ListView):
    model = Event
    template_name = 'lecturer/lecturercalendar.html'
 
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