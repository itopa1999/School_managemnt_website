from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import *
from .forms import *
from users.models import User
from administrator.models import *
from administrator.forms import *
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from administrator.utils import Calendar
from administrator.decorators import *

 
# Create your views here.


@login_required(login_url='login')
@supervisor_only
def  supervisordashboard(request):
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
    return render(request,'supervisor/supervisordashboard.html',context)


@login_required(login_url='login')
@supervisor_only
def  supviewprofile(request):
    user=User.objects.get(id=request.user.id)
    form = UserForm1(instance=user)
    if request.method =='POST':
        form = UserForm1(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('supviewprofile')
        else:
            messages.error(request, "form error")
            return redirect('supviewprofile')
    context = {'form':form}
    return render(request,'supervisor/supviewprofile.html', context)



@login_required(login_url='login')
@supervisor_only
def  supexamrecord(request):
    user=User.objects.filter(id=request.user.id)
    name=user[0].first_name
    form=RecordForm()
    if request.method=='POST':
        form=RecordForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
            course=Course.objects.get(id=request.POST.get('courseID'))
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.faculty=faculty
            form.course=course
            form.department=department
            form.supervisor=name
            form.save()
            messages.success(request, 'Record has been submitted')
            return redirect('supexamrecord')
    context={'form':form}
    return render(request,'supervisor/supexamrecord.html',context)

 

@login_required(login_url='login')
@supervisor_only
def  malpractice(request):
    user=User.objects.filter(id=request.user.id)
    name=user[0].first_name
    form=MalpracticeForm()
    if request.method=='POST':
        form=MalpracticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            student=Student.objects.get(id=request.POST.get('studentID'))
            form.student=student
            form.course=course
            form.supervisor=name
            user=form.save()
            messages.success(request, 'Malpracticism student has been submitted')
            return redirect('malpractice')
        else:
            messages.error(request, 'Form error')
            return redirect('malpractice')
    context={'form':form}
    return render(request,'supervisor/malpractice.html',context)



@login_required(login_url='login')
@supervisor_only
def  supchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('supchangepassword')
    context={'form':form}
    return render(request,'supervisor/supchangepassword.html',context)



@login_required(login_url='login')
@supervisor_only
def  supviewfaculty(request):
    fac=Faculty.objects.all()
    context = {'fac':fac}
    return render(request, 'supervisor/supviewfaculty.html', context)


@login_required(login_url='login')
@supervisor_only
def  supfaculty(request, pk_profile2):
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
    return render(request, 'supervisor/supfaculty.html', context)


@login_required(login_url='login')
@supervisor_only
def  supviewdepartment(request):
    dep=Department.objects.all()
    context = {'dep':dep}
    return render(request,'supervisor/supviewdepartment.html',context)



@login_required(login_url='login')
@supervisor_only
def  supdepartment(request, pk_profile3):
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
    return render(request, 'supervisor/supdepartment.html', context)




@login_required(login_url='login')
@supervisor_only
def  supalllecturers(request):
    lec= Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'supervisor/supalllecturers.html',context)


@login_required(login_url='login')
@supervisor_only
def  supallstudents(request):
    stu= Student.objects.all().order_by('adm_year')
    context={'stu':stu}
    return render(request,'supervisor/supallstudents.html',context)


@login_required(login_url='login')
@supervisor_only
def  supviewcourse(request):
    dep=Department.objects.all()
    context={'dep':dep}
    return render(request, 'supervisor/supviewcourse.html', context)


@login_required(login_url='login')
@supervisor_only
def  supeviewcourse(request,pk):
    dep=Department.objects.get(id=pk)
    cou=Course.objects.filter(department=dep)
    if not cou:
        messages.info(request, 'there is no course in this department here')
        return redirect('supviewcourse')
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
    return render(request, 'supervisor/supeviewcourse.html', context)


@login_required(login_url='login')
@supervisor_only
def  supnoticeboard(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'supervisor/supnoticeboard.html',context)


@login_required(login_url='login')
@supervisor_only
def  supsentmessage(request):
    user=User.objects.get(id=request.user.id)
    meg=Message.objects.filter(sender=user)
    context={'meg':meg}
    return render(request, 'supervisor/supsentmessage.html',context)



@login_required(login_url='login')
@supervisor_only
def  supdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('supsentmessage')



@login_required(login_url='login')
@supervisor_only
def supviewmessage(request):
    user3=Group.objects.get(name="supervisor")
    meg= Message.objects.filter(group=user3)    
    context={'meg':meg}
    return render(request, 'supervisor/supviewmessage.html', context)

@login_required(login_url='login')
@supervisor_only
def supnewmessage(request):
    form= MessageForm()
        
    context={'form':form}
    return render(request, 'supervisor/supnewmessage.html', context)



@login_required(login_url='login')
@supervisor_only
def  suptemplate1(request):
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
           return redirect('suptemplate1') 
        else:
            messages.error(request, 'Message error')
            return redirect('suptemplate1') 
    context={'form':form}
    return render(request, 'supervisor/suptemplate1.html', context)


@login_required(login_url='login')
@supervisor_only
def  suptemplate2(request):
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
           return redirect('suptemplate2') 
        else:
            messages.error(request, 'Message error')
            return redirect('suptemplate2') 
    context={'form':form}
    return render(request, 'supervisor/suptemplate2.html', context)


@login_required(login_url='login')
@supervisor_only
def  suptemplate3(request):
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
           return redirect('suptemplate3') 
        else:
            messages.error(request, 'Message error')
            return redirect('suptemplate3') 
    context={'form':form}
    return render(request, 'supervisor/suptemplate3.html', context)


@login_required(login_url='login')
@supervisor_only
def  suptemplate4(request):
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
           return redirect('suptemplate4') 
        else:
            messages.error(request, 'Message error')
            return redirect('suptemplate4') 
    context={'form':form}
    return render(request, 'supervisor/suptemplate4.html', context)


@login_required(login_url='login')
@supervisor_only
def  supdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('supsentmessage')


@login_required(login_url='login')
@supervisor_only
def  supexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'supervisor/supexamtable.html',context)



@login_required(login_url='login')
@supervisor_only
def  supstatus(request):
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
                return redirect('supstatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('supstatus')
        else:
            messages.error(request, 'form error')
            return redirect('supstatus')
    context={'form':form}
    return render(request,'supervisor/supstatus.html',context)


@login_required(login_url='login')
@supervisor_only
def  supdeletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('supviewstatus')


@login_required(login_url='login')
@supervisor_only
def  supviewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'supervisor/supviewstatus.html',context)



class supCalendarView(generic.ListView):
    model = Event
    template_name = 'supervisor/supCalendarView.html'
 
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


