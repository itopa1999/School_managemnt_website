from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from library import models as MYMODEL
from .forms import *
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib import auth
from administrator.models import *
from administrator.forms import *
from users.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.views import generic
from django.utils.safestring import mark_safe
from administrator.utils import Calendar
from administrator.decorators import *

# Create your views here.


@login_required(login_url='login')
@library_only
def  librarydashboard(request):
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
    return render(request,'library/librarydashboard.html',context)


    



@login_required(login_url='login')
@library_only
def  addbook(request):
    form=BookForm()
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            dep=Department.objects.get(id=request.POST.get('departmentID'))
            form.department=dep
            form.save()
            messages.success(request, 'book has been added to shelf')
            return redirect('addbook')
        else:
            messages.error(request, 'form error')
            return redirect('addbook')
    return render(request,'library/addbook.html',{'form':form})




@login_required(login_url='login')
@library_only
def  libviewbook(request):
    books=MYMODEL.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})





@login_required(login_url='login')
@library_only
def  issuebook(request):
    form=IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            stu=MYMODEL.Student.objects.get(id=request.POST.get('studentID'))
            stu1=MYMODEL.Student.objects.filter(name=stu)
            dep=stu1[0].department
            obj.student=stu
            obj.department=dep
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            messages.success(request, 'book has been issued to ' + str (stu))
            return redirect('issuebook')
        else:
            messages.error(request, 'form error')
            return redirect('issuebook')
    return render(request,'library/issuebook.html',{'form':form})





@login_required(login_url='login')
@library_only
def   viewissuedbook(request):
    issuedbooks=MYMODEL.IssuedBook.objects.all()
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


        books=list(MYMODEL.Book.objects.filter(isbn=ib.isbn))
        students=list(MYMODEL.Student.objects.filter(department=ib.department))
        i=0
        for l in books:
            t=(students[i].name,students[i].department,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)
    messages.info(request, 'Fine will be given to student after 15days of issued books')
    return render(request,'library/viewissuedbook.html',{'li':li})



@login_required(login_url='login')
@library_only
def  viewstudent(request):
    students=MYMODEL.Student.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='login')
@library_only
def  libviewprofile(request):
    user=User.objects.get(id=request.user.id)
    form = UserForm1(instance=user)
    if request.method =='POST':
        form = UserForm1(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('libviewprofile')
        else:
            messages.error(request, "form error")
            return redirect('libviewprofile')
    context = {'form':form}
    return render(request,'library/libviewprofile.html',context)




@login_required(login_url='login')
@library_only
def  libchangepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('libchangepassword')
    context={'form':form}
    return render(request,'library/libchangepassword.html',context)



@login_required(login_url='login')
@library_only
def  libnoticeboard(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'library/libnoticeboard.html',context)



@login_required(login_url='login')
@library_only
def  libsentmessage(request):
    user=User.objects.get(id=request.user.id)
    meg=Message.objects.filter(sender=user)
    context={'meg':meg}
    return render(request, 'library/libsentmessage.html',context)



@login_required(login_url='login')
@library_only
def  libdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('libsentmessage')



@login_required(login_url='login')
@library_only
def libviewmessage(request):
    user3=Group.objects.get(name="library")
    meg= Message.objects.filter(group=user3)    
    context={'meg':meg}
    return render(request, 'library/libviewmessage.html', context)




@login_required(login_url='login')
@library_only
def libnewmessage(request):
    form= MessageForm()
        
    context={'form':form}
    return render(request, 'library/libnewmessage.html', context)



@login_required(login_url='login')
@library_only
def  libtemplate1(request):
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
           return redirect('libtemplate1') 
        else:
            messages.error(request, 'Message error')
            return redirect('libtemplate1') 
    context={'form':form}
    return render(request, 'library/libtemplate1.html', context)


@login_required(login_url='login')
@library_only
def  libtemplate2(request):
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
           return redirect('libtemplate2') 
        else:
            messages.error(request, 'Message error')
            return redirect('libtemplate2') 
    context={'form':form}
    return render(request, 'library/libtemplate2.html', context)


@login_required(login_url='login')
@library_only
def  libtemplate3(request):
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
           return redirect('libtemplate3') 
        else:
            messages.error(request, 'Message error')
            return redirect('libtemplate3') 
    context={'form':form}
    return render(request, 'library/libtemplate3.html', context)


@login_required(login_url='login')
@library_only
def  libtemplate4(request):
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
           return redirect('libtemplate4') 
        else:
            messages.error(request, 'Message error')
            return redirect('libtemplate4') 
    context={'form':form}
    return render(request, 'library/libtemplate4.html', context)


@login_required(login_url='login')
@library_only
def  libdeletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('libsentmessage')


@login_required(login_url='login')
@library_only
def  libexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'library/libexamtable.html',context)


@login_required(login_url='login')
@library_only
def  libtable(request):
    tim=Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request,'library/libtable.html',context)


@login_required(login_url='login')
@library_only
def  libstatus(request):
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
                return redirect('libstatus')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('libstatus')
        else:
            messages.error(request, 'form error')
            return redirect('libstatus')
    context={'form':form}
    return render(request,'library/libstatus.html',context)


@login_required(login_url='login')
@library_only
def  libdeletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('libviewstatus')


@login_required(login_url='login')
@library_only
def  libviewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'library/libviewstatus.html',context)



class libCalendarView(generic.ListView):
    model = Event
    template_name = 'library/libcalendar.html'
 
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

