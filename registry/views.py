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
@registry_only
def  adminstu(request):
    stu= Student.objects.all()
    myFilter=AccessFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    context={'stu':stu,"myFilter":myFilter}
    return render(request, 'registry/adminstu.html', context)


@login_required(login_url='login')
@registry_only
def appadmission(request,pk):
    student=Student.objects.get(id=pk)
    student.adminstatus=True
    student.save()
    messages.success(request, 'Student has been given admission')
    return redirect('adminstu')

@login_required(login_url='login')
@registry_only
def disadmission(request,pk):
    student=Student.objects.get(id=pk)
    student.adminstatus=False
    student.save()
    messages.success(request, ' Admission has been revoke successfully')
    return redirect('adminstu')



@login_required(login_url='login')
@registry_only
def  registrydashboard(request):
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
    return render(request,'registry/registrydashboard.html',context)


@login_required(login_url='login')
@registry_only
def  regviewprofile(request):
    user=User.objects.get(id=request.user.id)
    form = UserForm1(instance=user)
    if request.method =='POST':
        form = UserForm1(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('regviewprofile')
        else:
            messages.error(request, "form error")
            return redirect('regviewprofile')
    context = {'form':form}
    return render(request,'registry/regviewprofile.html',context)



@login_required(login_url='login')
@registry_only
def  regchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('regchangepassword')
    context={'form':form}
    return render(request,'registry/regchangepassword.html',context)



@login_required(login_url='login')
@registry_only
def  regviewfaculty(request):
    fac=Faculty.objects.all()
    context = {'fac':fac}
    return render(request, 'registry/regviewfaculty.html', context)


@login_required(login_url='login')
@registry_only
def  regfaculty(request, pk_profile2):
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
    return render(request, 'registry/regfaculty.html', context)


@login_required(login_url='login')
@registry_only
def  regviewdepartment(request):
    dep=Department.objects.all()
    context = {'dep':dep}
    return render(request,'registry/regviewdepartment.html',context)



@login_required(login_url='login')
@registry_only
def  regdepartment(request, pk_profile3):
    dep=Department.objects.get(id=pk_profile3)
    depu = Department.objects.get(id=pk_profile3)
    countstu=Student.objects.filter(department=pk_profile3).count()
    stu=Student.objects.filter(department=pk_profile3)
    hnd= stu.filter(level='HND').count()
    nd= stu.filter(level='ND').count()
    pt= stu.filter(program='Part time').count()
    ft= stu.filter(program='Full time').count()
    if request.method == "POST":
        dep.delete()
        return redirect('dashboard')
    context= {'dep':dep,'item':dep,'depu':depu,
              'countstu':countstu,'hnd':hnd,'nd':nd,'pt':pt,
              'ft':ft}
    return render(request, 'registry/regdepartment.html', context)




@login_required(login_url='login')
@registry_only
def  regalllecturers(request):
    lec= Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'registry/regalllecturers.html',context)


@login_required(login_url='login')
@registry_only
def  reglecturer(request, pk_profile1):
    lec=Lecturer.objects.get(id=pk_profile1)
    fil=File2.objects.filter(lecturer=pk_profile1)
    work=Work_Experience1.objects.filter(lecturer=pk_profile1)
    ins=Institution_Attended1.objects.filter(lecturer=pk_profile1)
    sta=Status.objects.filter(user=lec)
    cou=Course.objects.filter(lecturer=lec)
    context={'lec':lec, 'item':lec,'fil':fil,'work':work,
             'ins':ins,'sta':sta,'cou':cou}
    return render(request, 'registry/reglecturer.html', context)


@login_required(login_url='login')
@registry_only
def  reglectureresult(request,pk):
    lec=Lecturer.objects.get(id=pk)
    res=LecturerResult.objects.filter(lecturer=lec).order_by('date')
    if not res:
        messages.info(request, 'Lecturer has not submitted any student result yet')
        return redirect('reglecturerview')
    context={'res':res}
    return render(request, 'registry/reglectureresult.html', context)


@login_required(login_url='login')
@registry_only
def  reglecturerview(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request, 'registry/reglecturerview.html', context)


@login_required(login_url='login')
@registry_only
def  regattendance(request):
    att=Attendance.objects.all().order_by('date')
    context={'att':att}
    return render(request,'registry/regattendance.html',context)


@login_required(login_url='login')
@registry_only
def  regallstudents(request):
    stu= Student.objects.all().order_by('adm_year')
    context={'stu':stu}
    return render(request,'registry/regallstudents.html',context)


@login_required(login_url='login')
@registry_only
def  regstudent(request, pk_profile):
    stud=Student.objects.filter(id=pk_profile)
    dep=stud[0].department
    stu=Student.objects.get(id=pk_profile)
    ndstudent=Student.objects.filter(id=pk_profile,level="ND")
    sch=Schoollevy.objects.all()
    re=Result.objects.filter(student=pk_profile)
    fil=File.objects.filter(student=pk_profile).exclude(title="passport")
    pas=File.objects.filter(student=pk_profile).filter(title="passport")
    cou=Register_course.objects.filter(student=stu)
    sta=Status.objects.filter(user=stu)
    context={'stu':stu,'sch':sch, 'item':stu,'fil':fil,'pas':pas,
             'cou':cou,'sta':sta} 
    return render(request, 'registry/regstudent.html', context)


@login_required(login_url='login')
@registry_only
def  regstudentmark(request):
    stu= Student.objects.all()
    context={'stu':stu}
    return render(request,'registry/regstudentmark.html',context)


@login_required(login_url='login')
@registry_only
def  regmarks(request,pk):
    stu=Student.objects.get(id=pk)
    res=Result1.objects.filter(student=stu)
    cou =Course.objects.filter(result1__student=stu)
    if not cou:
        messages.info(request, 'There is no exam result for this student yet')
        return redirect('regstudentmark')
    context={'cou':cou}
    response =  render(request,'registry/regmarks.html',context)
    response.set_cookie('student_id',str(pk))
    return response


@login_required(login_url='login')
@registry_only
def  regcheckmarks(request,pk):
    course =Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    student_id = request.COOKIES.get('student_id')
    student= Student.objects.get(id=student_id)
    res= Result1.objects.all().filter(course=course).filter(student=student)
    context={'res':res,'total_marks':total_marks}
    return render(request,'registry/regcheckmarks.html',context)



@login_required(login_url='login')
@registry_only
def  regviewresult(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'registry/regviewresult.html', context)


@login_required(login_url='login')
@registry_only
def  regadminsturesult(request, pk):
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
    return render(request, 'registry/regadminsturesult.html', context)




@login_required(login_url='login')
@registry_only
def  regviewcourse(request):
    dep=Department.objects.all()
    context={'dep':dep}
    return render(request, 'registry/regviewcourse.html', context)


@login_required(login_url='login')
@registry_only
def  regdviewcourse(request,pk):
    dep=Department.objects.get(id=pk)
    cou=Course.objects.filter(department=dep)
    if not cou:
        messages.info(request, 'there is no course in this department here')
        return redirect('regviewcourse')
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
    return render(request, 'registry/regdviewcourse.html', context)


@login_required(login_url='login')
@registry_only
def  regtransactions(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'registry/regtransactions.html', context)


@login_required(login_url='login')
@registry_only
def regsummary(request,pk):
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
    return render(request, 'registry/regsummary.html', context=mydict)






@login_required(login_url='login')
@registry_only
def  regcreditpayment(request):
    stu=Student.objects.all()
    user=User.objects.get(id=request.user.id)
    form= CreditForm()
    if request.method == 'POST':
        form =  CreditForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=user
            tra=Transaction.objects.filter(student=form.student,schoollevy=form.schoollevy)
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
            if bal >= -1:
                messages.error(request, 'you are inputting the wrong value')
                return redirect('regcreditpayment')
            else:
                form.save()
                messages.success(request, 'student has been debited successfully')
                return redirect('regcreditpayment') 
    context={'form':form,'stu':stu}
    return render(request, 'registry/regcreditpayment.html', context)



@login_required(login_url='login')
@registry_only
def regdebitpayment(request):
    stu=Student.objects.all()
    user=User.objects.get(id=request.user.id)
    form= DebitForm()
    if request.method == 'POST':
        name=request.POST.get('tra.name')
        print(name)
        form =  DebitForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            form.user=user
            tra=Transaction.objects.filter(student=form.student,schoollevy=form.schoollevy)
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
            if bal >= -1:
                messages.error(request, 'you are inputting the wrong value')
                return redirect('regdebitpayment')
            else:
                form.save()
                messages.success(request, 'student has been debited successfully')
                return redirect('debitpayment') 
    context={'form':form,'stu':stu}
    return render(request, 'registry/regdebitpayment.html', context)





@login_required(login_url='login')
@registry_only
def  regnoticeboard(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'registry/regnoticeboard.html',context)


@login_required(login_url='login')
@registry_only
def  regdeletenotice(request,pk):
    notice=Notice.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('regnoticeboard')


@login_required(login_url='login')
@registry_only
def  regnewnotice(request):
    user1 =User.objects.filter(id=request.user.id)
    pic=user1[0].profile_pic
    user =User.objects.get(id=request.user.id)
    form=NoticeForm()
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.profile_pic=pic
            form.sender=user
            form.save()
            messages.success(request, 'Notice has been pasted to noticeboard')
            return redirect('regnewnotice')
        else:
            messages.error(request, 'form error')
            return redirect('regnewnotice')
    context={'form':form}
    return render(request,'registry/regnewnotice.html',context)



@login_required(login_url='login')
@registry_only
def  regresult(request):
    form=ResultForm()
    if request.metreg == 'POST':
        form= ResultForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            student=Student.objects.get(id=request.POST.get('studentID'))
            form.student=student
            form.course=course
            form.save()
            messages.success(request, 'result has been added to student result')
            return redirect('regresult')
        else:
            messages.error(request, 'form error')
            return redirect('regresult')
    context= {'form':form}   
    return render(request, 'registry/regresult.html', context)





@login_required(login_url='login')
@registry_only
def  regsentmessage(request):
    user=User.objects.get(id=request.user.id)
    meg=Message.objects.filter(sender=user)
    context={'meg':meg}
    return render(request, 'registry/regsentmessage.html',context)

@login_required(login_url='login')
@registry_only
def  regdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('regsentmessage')



@login_required(login_url='login')
@registry_only
def regviewmessage(request):
    user3=Group.objects.get(name="registry")
    meg= Message.objects.filter(group=user3)    
    context={'meg':meg}
    return render(request, 'registry/regviewmessage.html', context)




@login_required(login_url='login')
@registry_only
def regnewmessage(request):
    form= MessageForm()
        
    context={'form':form}
    return render(request, 'registry/regnewmessage.html', context)



@login_required(login_url='login')
@registry_only
def  regtemplate1(request):
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
           return redirect('regtemplate1') 
        else:
            messages.error(request, 'Message error')
            return redirect('regtemplate1') 
    context={'form':form}
    return render(request, 'registry/regtemplate1.html', context)


@login_required(login_url='login')
@registry_only
def  regtemplate2(request):
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
           return redirect('regtemplate2') 
        else:
            messages.error(request, 'Message error')
            return redirect('regtemplate2') 
    context={'form':form}
    return render(request, 'registry/regtemplate2.html', context)


@login_required(login_url='login')
@registry_only
def  regtemplate3(request):
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
           return redirect('regtemplate3') 
        else:
            messages.error(request, 'Message error')
            return redirect('regtemplate3') 
    context={'form':form}
    return render(request, 'registry/regtemplate3.html', context)


@login_required(login_url='login')
@registry_only
def  regtemplate4(request):
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
           return redirect('regtemplate4') 
        else:
            messages.error(request, 'Message error')
            return redirect('regtemplate4') 
    context={'form':form}
    return render(request, 'registry/regtemplate4.html', context)


@login_required(login_url='login')
@registry_only
def  regdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('regsentmessage')


@login_required(login_url='login')
@registry_only
def  regexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'registry/regexamtable.html',context)


@login_required(login_url='login')
@registry_only
def  regtable(request):
    tim=Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'registry/regtable.html',context)


@login_required(login_url='login')
@registry_only
def  regstatus(request):
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
                return redirect('regstatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('regstatus')
        else:
            messages.error(request, 'form error')
            return redirect('regstatus')
    context={'form':form}
    return render(request,'registry/regstatus.html',context)


@login_required(login_url='login')
@registry_only
def  regdeletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('regviewstatus')


@login_required(login_url='login')
@registry_only
def  regviewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'registry/regviewstatus.html',context)



class regCalendarView(generic.ListView):
    model = Event
    template_name = 'registry/regCalendarView.html'
 
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


