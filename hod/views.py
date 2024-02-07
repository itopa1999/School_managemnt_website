from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import *
from .forms import *
from users.models import User
from administrator.models import *
from administrator.forms import *
from administrator.filters import *
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from administrator.utils import Calendar
from administrator.decorators import *

# Create your views here.

@login_required(login_url='login')
@hod_only
def hoddashboard(request):
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
    return render(request,'hod/hoddashboard.html',context)


@login_required(login_url='login')
@hod_only
def hodviewprofile(request):
    user=User.objects.get(id=request.user.id)
    form = UserForm1(instance=user)
    if request.method =='POST':
        form = UserForm1(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('hodviewprofile')
        else:
            messages.error(request, "form error")
            return redirect('hodviewprofile')
    context = {'form':form}
    return render(request,'hod/hodviewprofile.html',context)


@login_required(login_url='login')
@hod_only
def hodchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('hodchangepassword')
    context={'form':form}
    return render(request,'hod/hodchangepassword.html',context)



@login_required(login_url='login')
@hod_only
def hodviewfaculty(request):
    fac=Faculty.objects.all()
    context = {'fac':fac}
    return render(request, 'hod/hodviewfaculty.html', context)


@login_required(login_url='login')
@hod_only
def hodfaculty(request, pk_profile2):
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
    return render(request, 'hod/hodfaculty.html', context)



@login_required(login_url='login')
@hod_only
def hodviewdepartment(request):
    dep=Department.objects.all()
    context = {'dep':dep}
    return render(request,'hod/hodviewdepartment.html',context)



@login_required(login_url='login')
@hod_only
def hoddepartment(request, pk_profile3):
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
    return render(request, 'hod/hoddepartment.html', context)


@login_required(login_url='login')
@hod_only
def hodalllecturers(request):
    lec= Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'hod/hodalllecturers.html',context)


@login_required(login_url='login')
@hod_only
def hodlecturer(request, pk_profile1):
    lec=Lecturer.objects.get(id=pk_profile1)
    fil=File2.objects.filter(lecturer=pk_profile1)
    work=Work_Experience1.objects.filter(lecturer=pk_profile1)
    ins=Institution_Attended1.objects.filter(lecturer=pk_profile1)
    sta=Status.objects.filter(user=lec)
    cou=Course.objects.filter(lecturer=lec)
    context={'lec':lec, 'item':lec,'fil':fil,'work':work,
             'ins':ins,'sta':sta,'cou':cou}
    return render(request, 'hod/hodlecturer.html', context)


@login_required(login_url='login')
@hod_only
def hodlectureresult(request,pk):
    lec=Lecturer.objects.get(id=pk)
    res=LecturerResult.objects.filter(lecturer=lec).order_by('date')
    if not res:
        messages.info(request, 'Lecturer has not submitted any student result yet')
        return redirect('hodlecturerview')
    context={'res':res}
    return render(request, 'hod/hodlectureresult.html', context)


@login_required(login_url='login')
@hod_only
def hodlecturerview(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request, 'hod/hodlecturerview.html', context)


@login_required(login_url='login')
@hod_only
def hodattendance(request):
    att=Attendance.objects.all().order_by('date')
    context={'att':att}
    return render(request,'hod/hodattendance.html',context)


@login_required(login_url='login')
@hod_only
def hodallstudents(request):
    stu= Student.objects.all().order_by('adm_year')
    context={'stu':stu}
    return render(request,'hod/hodallstudents.html',context)



@login_required(login_url='login')
@hod_only
def hodstudent(request, pk_profile):
    stud=Student.objects.filter(id=pk_profile)
    dep=stud[0].department
    stu=Student.objects.get(id=pk_profile)
    ndstudent=Student.objects.filter(id=pk_profile,level="ND")
    sch=Schoollevy.objects.all()
    re=Result.objects.filter(student=pk_profile)
    fil=File.objects.filter(student=pk_profile)
    pas=File.objects.filter(student=pk_profile)
    cou=Register_course.objects.filter(student=stu)
    sta=Status.objects.filter(user=stu)
    context={'stu':stu,'sch':sch, 'item':stu,'fil':fil,'pas':pas,
             'cou':cou,'sta':sta}
    return render(request, 'hod/hodstudent.html', context)



@login_required(login_url='login')
@hod_only
def hodstudentmark(request):
    stu= Student.objects.all()
    context={'stu':stu}
    return render(request,'hod/hodstudentmark.html',context)



@login_required(login_url='login')
@hod_only
def hodmarks(request,pk):
    stu=Student.objects.get(id=pk)
    res=Result1.objects.filter(student=stu)
    cou =Course.objects.filter(result1__student=stu)
    if not cou:
        messages.info(request, 'There is no exam result for this student yet')
        return redirect('hodstudentmark')
    context={'cou':cou}
    response =  render(request,'hod/hodmarks.html',context)
    response.set_cookie('student_id',str(pk))
    return response


@login_required(login_url='login')
@hod_only
def hodcheckmarks(request,pk):
    course =Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    student_id = request.COOKIES.get('student_id')
    student= Student.objects.get(id=student_id)
    res= Result1.objects.all().filter(course=course).filter(student=student)
    context={'res':res,'total_marks':total_marks}
    return render(request,'hod/hodcheckmarks.html',context)


@login_required(login_url='login')
@hod_only
def hodviewresult(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'hod/hodviewresult.html', context)


@login_required(login_url='login')
@hod_only
def hodadminsturesult(request, pk):
    stud=Student.objects.filter(id=pk)
    dep=stud[0].department
    stu=Student.objects.get(id=pk)
    ndstudent=Student.objects.filter(id=pk,level="ND")
    sch=Schoollevy.objects.all()
    re=Result.objects.filter(student=pk)
    if ndstudent:
        res=re.filter(course__semester="ND1 first Semester",course__department=dep)
        res1=re.filter(course__semester="ND1 second Semester",course__department=dep)
        res2=re.filter(course__semester="ND2 first Semester",course__department=dep)
        res3=re.filter(course__semester="ND2 second Semester",course__department=dep)
        tit="ND1 FIRST SEMESTER"
        tit1="ND1 SECOND SEMESTER"
        tit2="ND2 FIRST SEMESTER"
        tit3="ND2 SECOND SEMESTER"
        ti="ND1"
        ti1="ND2"
    else:
        res=re.filter(course__semester="HND1 first Semester",course__department=dep)
        res1=re.filter(course__semester="HND1 second Semester",course__department=dep)
        res2=re.filter(course__semester="HND2 first Semester",course__department=dep)
        res3=re.filter(course__semester="HND2 second Semester",course__department=dep)
        tit="HND1 FIRST SEMESTER"
        tit1="HND1 SECOND SEMESTER"
        tit2="HND2 FIRST SEMESTER"
        tit3="HND2 SECOND SEMESTER"
        ti='HND1'
        ti1="HND2"
    qp=res.aggregate(Sum('qp'))['qp__sum']
    cu=res.aggregate(Sum('cu'))['cu__sum']
    qp1=res1.aggregate(Sum('qp'))['qp__sum']
    cu1=res1.aggregate(Sum('cu'))['cu__sum']
    qp2=res2.aggregate(Sum('qp'))['qp__sum']
    cu2=res2.aggregate(Sum('cu'))['cu__sum']
    qp3=res3.aggregate(Sum('qp'))['qp__sum']
    cu3=res3.aggregate(Sum('cu'))['cu__sum']
    if qp  is None and cu is None:
        gpa=0
    else:
        gpa=qp/cu
    if qp1  is None and cu1 is None:
        gpa1=0
    else:
        gpa1=qp1/cu1
    
    if gpa==0 or gpa1==0:
        cgpa=0
    else:
        cgpa=gpa/gpa1    
    
    if qp2  is None and cu2 is None:
        gpa2=0
    else:
        gpa2=qp2/cu2
    if qp3  is None and cu3 is None:
        gpa3=0
    else:
        gpa3=qp3/cu3
    
    if gpa2==0 or gpa3==0:
        cgpa2=0
    else:
        cgpa2=gpa2/gpa3
        
    if cgpa==0 or cgpa2==0:
        messages.info(request, ' Total cgpa will not be calculated, invalid input')
        cgpa1=0
    else:
        cgpa1=cgpa/cgpa2
        
        
        
        
        
    if gpa >=3.50:
        grade=("DISTINCTION")
    elif gpa <=3.49 and gpa >=3.00:
        grade =("UPPER CREDIT")
    elif gpa <=2.99 and gpa >=2.50:
        grade =("LOWER CREDIT")
    elif gpa <=2.49 and gpa >=2.00:
        grade =("PASS")
    elif gpa <=1.99 and gpa >=0.01:
        grade =("FAIL")
    else:
        grade =''
        
        
    if gpa1 >=3.50:
        grade1=("DISTINCTION")
    elif gpa1 <=3.49 and gpa1 >=3.00:
        grade1 =("UPPER CREDIT")
    elif gpa1 <=2.99 and gpa1 >=2.50:
        grade1 =("LOWER CREDIT")
    elif gpa1 <=2.49 and gpa1 >=2.00:
        grade1 =("PASS")
    elif gpa1 <=1.99 and gpa1 >=0.01:
        grade1 =("FAIL")
    else:
        grade1 =''
        
    if gpa2 >=3.50:
        grade2=("DISTINCTION")
    elif gpa2 <=3.49 and gpa2 >=3.00:
        grade2 =("UPPER CREDIT")
    elif gpa2 <=2.99 and gpa2 >=2.50:
        grade2 =("LOWER CREDIT")
    elif gpa2 <=2.49 and gpa2 >=2.00:
        grade2 =("PASS")
    elif gpa2 <=1.99 and gpa2 >=0.01:
        grade2 =("FAIL")
    else:
        grade2 =''
        
    if gpa3 >=3.50:
        grade3=("DISTINCTION")
    elif gpa3 <=3.49 and gpa3 >=3.00:
        grade3 =("UPPER CREDIT")
    elif gpa3 <=2.99 and gpa3 >=2.50:
        grade3 =("LOWER CREDIT")
    elif gpa3 <=2.49 and gpa3 >=2.00:
        grade3 =("PASS")
    elif gpa3 <=1.99 and gpa3 >=0.01:
        grade3 =("FAIL")
    else:
        grade3 =''
    context={'stu':stu,'res':res,'res1':res1,'res2':res2,'res3':res3,
             'gpa':gpa,'gpa1':gpa1,'gpa2':gpa2,'gpa3':gpa3,'tit':tit,
             'tit1':tit1,'tit2':tit2,'tit3':tit3,'ti':ti,'ti1':ti1,
             'grade':grade,'grade1':grade1,'grade2':grade2,'grade3':grade3,
             'cgpa':cgpa,'cgpa2':cgpa2,'cgpa1':cgpa1}
    return render(request, 'hod/hodadminsturesult.html', context)


@login_required(login_url='login')
@hod_only
def hodviewcourse(request):
    dep=Department.objects.all()
    context={'dep':dep}
    return render(request, 'hod/hodviewcourse.html', context)



@login_required(login_url='login')
@hod_only
def hoddviewcourse(request,pk):
    dep=Department.objects.get(id=pk)
    cou=Course.objects.filter(department=dep)
    if not cou:
        messages.info(request, 'there is no course in this department here')
        return redirect('hodviewcourse')
    res=cou.filter(semester="ND1 first Semester")
    res1=cou.filter(semester="ND1 second Semester")
    res2=cou.filter(semester="ND2 first Semester")
    res3=cou.filter(semester="ND2 second Semester")
    res4=cou.filter(semester="HND1 first Semester")
    res5=cou.filter(semester="HND1 second Semester")
    res6=cou.filter(semester="HND2 first Semester")
    res7=cou.filter(semester="HND2 second Semester")
    context= {'cou':cou,'res':res,'res1':res1,'res2':res2,'res3':res3,
              'res4':res4,'res5':res5,'res6':res6,
             'res7':res7}
    return render(request, 'hod/hoddviewcourse.html', context)


@login_required(login_url='login')
@hod_only
def hodtransactions(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'hod/hodtransactions.html', context)


@login_required(login_url='login')
@hod_only
def hodsummary(request,pk):
    stu=Student.objects.get(id=pk)
    tra=Transaction.objects.filter(student=stu)
    myFilter=DebitFilter(request.GET, queryset=tra)
    tra=myFilter.qs
    total_paid=tra.aggregate(Sum('debit'))['debit__sum']
    total_credit=tra.aggregate(Sum('credit'))['credit__sum']
    #if total_paid is None and total_credit is None:
       # messages.error(request,'There is no transaction')
       # return redirect('transaction')
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
          'total_credit':total_credit,'bal':bal,'stu':stu,'myFilter':myFilter
    }
    return render(request, 'hod/hodsummary.html', context=mydict)




@login_required(login_url='login')
@hod_only
def hodnoticeboard(request):
    context={}
    return render(request,'hod/hodnoticeboard.html',context)



@login_required(login_url='login')
@hod_only
def hodnewnotice1(request):
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
            return redirect('hodnewnotice1')
        else:
            messages.error(request, 'form error')
            return redirect('hodnewnotice1')
    context={'form':form}
    return render(request,'hod/hodnewnotice1.html',context)


@login_required(login_url='login')
@hod_only
def hoddepartmentnotice(request):
    notice=DepartmentNotice.objects.all()
    context={'notice':notice}
    return render(request,'hod/hoddepartmentnotice.html',context)


@login_required(login_url='login')
@hod_only
def hodgeneralnotice(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'hod/hodgeneralnotice.html',context)


@login_required(login_url='login')
@hod_only
def hoddeletedepnotice(request):
    notice=DepartmentNotice.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('hoddepartmentnotice')


@login_required(login_url='login')
@hod_only
def hodresult(request):
    form=ResultForm()
    if request.method == 'POST':
        form= ResultForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            cou=Course.objects.filter(name=course)
            cu=cou[0].course_unit
            student=Student.objects.get(id=request.POST.get('studentID'))
            form.student=student
            form.course=course
            form.cu=cu
            form.save()
            messages.success(request, 'result has been added to student result')
            return redirect('hodresult')
        else:
            messages.error(request, 'form error')
            return redirect('hodresult')
    context= {'form':form}   
    return render(request, 'hod/hodresult.html', context)



@login_required(login_url='login')
@hod_only
def hodsentmessage(request):
    user=User.objects.get(id=request.user.id)
    meg=Message.objects.filter(sender=user)
    context={'meg':meg}
    return render(request, 'hod/hodsentmessage.html',context)



@login_required(login_url='login')
@hod_only
def hodviewmessage(request):
    user2=Group.objects.get(name="hod")
    meg= Message.objects.filter(group=user2)    
    context={'meg':meg}
    return render(request, 'hod/hodviewmessage.html', context)

@login_required(login_url='login')
@hod_only
def hodnewmessage(request):
    form= MessageForm()
    context={'form':form}
    return render(request, 'hod/hodnewmessage.html', context)



@login_required(login_url='login')
@hod_only
def hodtemplate1(request):
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
           return redirect('hodtemplate1') 
        else:
            messages.error(request, 'Message error')
            return redirect('hodtemplate1') 
    context={'form':form}
    return render(request, 'hod/hodtemplate1.html', context)



@login_required(login_url='login')
@hod_only
def hodtemplate2(request):
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
           return redirect('hodtemplate2') 
        else:
            messages.error(request, 'Message error')
            return redirect('hodtemplate2') 
    context={'form':form}
    return render(request, 'hod/hodtemplate2.html', context)



@login_required(login_url='login')
@hod_only
def hodtemplate3(request):
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
           return redirect('hodtemplate3') 
        else:
            messages.error(request, 'Message error')
            return redirect('hodtemplate3') 
    context={'form':form}
    return render(request, 'hod/hodtemplate3.html', context)


@login_required(login_url='login')
@hod_only
def hodtemplate4(request):
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
           return redirect('hodtemplate4') 
        else:
            messages.error(request, 'Message error')
            return redirect('hodtemplate4') 
    context={'form':form}
    return render(request, 'hod/hodtemplate4.html', context)


@login_required(login_url='login')
@hod_only
def hoddeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('hodsentmessage')

@login_required(login_url='login')
@hod_only
def hodexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'hod/hodexamtable.html',context)


@login_required(login_url='login')
@hod_only
def hodtable(request):
    tim=Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'hod/hodtable.html',context)


@login_required(login_url='login')
@hod_only
def hodstatus(request):
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
                return redirect('hodstatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('hodstatus')
        else:
            messages.error(request, 'form error')
            return redirect('hodstatus')
    context={'form':form}
    return render(request,'hod/hodstatus.html',context)


@login_required(login_url='login')
@hod_only
def hoddeletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('hodviewstatus')


@login_required(login_url='login')
@hod_only
def hodviewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'hod/hodviewstatus.html',context)


@login_required(login_url='login')
@hod_only
def hodstucourse(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'hod/hodstucourse.html', context)


@login_required(login_url='login')
@hod_only
def hodcoursestudent(request, pk):
    stu=Student.objects.get(id=pk)
    ndstudent =Register_course.objects.filter(student=pk,student__level="ND")
    hndstudent =Register_course.objects.filter(student=pk,student__level="HND")
    if ndstudent:
        cou=Register_course.objects.filter(semester="ND1 first Semester")
        cou1=Register_course.objects.filter(semester="ND1 second Semester")
        cou2=Register_course.objects.filter(semester="ND2 first Semester")
        cou3=Register_course.objects.filter(semester="ND2 second Semester")
        tit="ND1 FIRST SEMESTER"
        tit1="ND1 SECOND SEMESTER"
        tit2="ND2 FIRST SEMESTER"
        tit3="ND2 SECOND SEMESTER"
    elif hndstudent:
        cou=Register_course.objects.filter(semester="HND1 first Semester")
        cou1=Register_course.objects.filter(semester="HND1 second Semester")
        cou2=Register_course.objects.filter(semester="HND2 first Semester")
        cou3=Register_course.objects.filter(semester="HND2 second Semester")
        tit="HND1 FIRST SEMESTER"
        tit1="HND1 SECOND SEMESTER"
        tit2="HND2 FIRST SEMESTER"
        tit3="HND2 SECOND SEMESTER"
    total=cou.aggregate(Sum('course_unit'))['course_unit__sum']
    total1=cou1.aggregate(Sum('course_unit'))['course_unit__sum']
    total2=cou2.aggregate(Sum('course_unit'))['course_unit__sum']
    total3=cou3.aggregate(Sum('course_unit'))['course_unit__sum']
    context={'cou':cou,'cou1':cou1,'cou2':cou2,'cou3':cou3,
             'tit':tit,'tit1':tit1,'tit2':tit2,'tit3':tit3,'stu':stu,
             'total':total,'total1':total1,'total2':total2,
             'total3':total3}
    return render(request, 'hod/hodcoursestudent.html', context)



class hodCalendarView(generic.ListView):
    model = Event
    template_name = 'hod/hodCalendarView.html'
 
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


