from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,timedelta
from django.core.exceptions import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *
from .decorators import *
from lecturer.forms import *
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.conf import settings
from datetime import date, timedelta
from django.db.models import Q
from student import models as SMODEL
from student import forms as SFORM
from lecturer import models as TMODEL
from lecturer import forms as TFORM
from users.models import User
from library import models as LMODEL
from supervisor import models as VMODEL
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar


# Create your views here.
@login_required(login_url='login')
@admin_only
def changegroup(request):
    group= Group.objects.get(name='student')
    user=User.objects.exclude(groups=group)
    context={'user':user}
    return render(request, 'Permissions/changegroup.html', context)


@login_required(login_url='login')
@admin_only
def groupchange(request,pk):
    user=User.objects.get(id=pk)
    form=GroupchangeForm(instance=user)
    if request.method=='POST':
        group=request.POST.get('groups')
        form=GroupchangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, ' has been added successfully ')
            return redirect('groupchange', user.id)
        else:
            messages.error(request, 'form error')
            return redirect('groupchange', user.id)
    context={'form':form,'user':user}
    return render(request, 'Permissions/groupchange.html', context)

      


@login_required(login_url='login')
@admin_only
def changepassword(request):
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
        form.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password has been changed successfully')
        return redirect('dashboard')
    context={'form':form}
    return render(request, 'Permissions/changepassword.html', context)




@login_required(login_url='login')
@admin_only
def access(request):
    context={}
    return render(request, 'Permissions/access.html', context)


@login_required(login_url='login')
@admin_only
def alllogin(request):
    Student.objects.all().update(access=False)
    messages.success(request, 'All Student has been Deactivated From accessing into this system')
    return redirect('access')


@login_required(login_url='login')
@admin_only
def alllogin1(request):
    Student.objects.all().update(access=True)
    messages.success(request, 'All Student has been re-activated for accessing into this system')
    return redirect('access')
    


@login_required(login_url='login')
@admin_only
def allexam(request):
    stu=Student.objects.all().update(examaccess=False)
    messages.success(request, 'All Student has been Deactivated From accessing result')
    return redirect('access')

    
@login_required(login_url='login')
@admin_only
def allexam1(request):
    stu=Student.objects.all().update(examaccess=True)
    messages.success(request, 'All Student has been re-activated for accessing result')
    return redirect('access')



@login_required(login_url='login')
@admin_only
def allresult(request):
    stu=Student.objects.all().update(resultaccess=False)
    messages.success(request, 'All Student has been Deactivated From accessing result')
    return redirect('access')


@login_required(login_url='login')
@admin_only
def allresult1(request):
    stu=Student.objects.all().update(resultaccess=True)
    messages.success(request, 'All Student has been re-activated for accessing result')
    return redirect('access')
    
    



@login_required(login_url='login')
@admin_only
def attaccess(request):
    sta= Lecturer.objects.all()
    myFilter=Access1Filter(request.GET, queryset=sta)
    sta=myFilter.qs
    context={'sta':sta,"myFilter":myFilter}
    return render(request,'Permissions/attaccess.html',context)


@login_required(login_url='login')
@admin_only
def disatt(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.attaccess=False
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been deactivated successfully')
    return redirect('attaccess')

@login_required(login_url='login')
@admin_only
def appatt(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.attaccess=True
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been activated successfully')
    return redirect('attaccess')


@login_required(login_url='login')
@admin_only
def loginaccess(request):
    stu= Student.objects.all()
    myFilter=AccessFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    context={'stu':stu,"myFilter":myFilter}
    return render(request,'Permissions/loginaccess.html',context)

@login_required(login_url='login')
@admin_only
def examaccess(request):
    stu= Student.objects.all()
    myFilter=AccessFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    context={'stu':stu,"myFilter":myFilter}
    return render(request,'Permissions/examaccess.html',context)

@login_required(login_url='login')
@admin_only
def loginaccess1(request):
    sta= Lecturer.objects.all()
    myFilter=Access1Filter(request.GET, queryset=sta)
    sta=myFilter.qs
    context={'sta':sta,"myFilter":myFilter}
    return render(request,'Permissions/loginaccess1.html',context)

@login_required(login_url='login')
@admin_only
def examaccess1(request):
    sta= Lecturer.objects.all()
    myFilter=Access1Filter(request.GET, queryset=sta)
    sta=myFilter.qs
    context={'sta':sta,"myFilter":myFilter}
    return render(request,'Permissions/examaccess1.html',context)


@login_required(login_url='login')
@admin_only
def resultaccess(request):
    stu= Student.objects.all()
    myFilter=AccessFilter(request.GET, queryset=stu)
    stu=myFilter.qs
    context={'stu':stu,"myFilter":myFilter}
    return render(request,'Permissions/resultaccess.html',context)

@login_required(login_url='login')
@admin_only
def disapproveaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.access=False
    student.save()
    messages.success(request, str(student) + ' has been deactivated successfully')
    return redirect('loginaccess')

@login_required(login_url='login')
@admin_only
def approveaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.access=True
    student.save()
    messages.success(request, str(student) + ' has been activated successfully')
    return redirect('loginaccess')


@login_required(login_url='login')
@admin_only
def disapproveexamaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.examaccess=False
    student.save()
    messages.success(request, str(student) + ' has been deactivated successfully')
    return redirect('examaccess')

@login_required(login_url='login')
@admin_only
def approveexamaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.examaccess=True
    student.save()
    messages.success(request, str(student) + ' has been activated successfully')
    return redirect('examaccess')


@login_required(login_url='login')
@admin_only
def disapproveaccess1(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.access=False
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been deactivated successfully')
    return redirect('loginaccess1')

@login_required(login_url='login')
@admin_only
def approveaccess1(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.access=True
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been activated successfully')
    return redirect('loginaccess1')


@login_required(login_url='login')
@admin_only
def disapproveexamaccess1(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.examaccess=False
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been deactivated successfully')
    return redirect('examaccess1')

@login_required(login_url='login')
@admin_only
def approveexamaccess1(request,pk):
    lecturer=Lecturer.objects.get(id=pk)
    lecturer.examaccess=True
    lecturer.save()
    messages.success(request, str(lecturer) + ' has been activated successfully')
    return redirect('examaccess1')

@login_required(login_url='login')
@admin_only
def disapproveresultaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.resultaccess=False
    student.save()
    messages.success(request, str(student) + ' has been deactivated successfully')
    return redirect('resultaccess')

@login_required(login_url='login')
@admin_only
def approveresultaccess(request,pk):
    student=Student.objects.get(id=pk)
    student.resultaccess=True
    student.save()
    messages.success(request, str(student) + ' has been activated successfully')
    return redirect('resultaccess')




@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin','admin','registry','bursary','hod','lecturer','library','supervisor'])
def loginsuccess(request):
    context = {}
    return render(request, 'Permissions/loginsuccess.html', context)

@login_required(login_url='login')
@admin_only
@admin_only
def registerlecturer(request):
    user3=User.objects.get(id=request.user.id)
    form = UserForm2()
    if request.method =='POST':
        form = UserForm2(request.POST)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user4=request.POST.get('user')
        user4=user3
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
        department=Department.objects.get(id=request.POST.get('departmentID'))
        if User.objects.filter(userid=userid):
            messages.error(request, "Staff_ID already exists")
            return redirect('registerlecturer')
        
        if User.objects.filter(first_name=first_name):
            messages.error(request, "Staff Name already exists")
            return redirect('registerlecturer')
        
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerlecturer')
        
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='lecturer')
            user.groups.add(group)
            
            Lecturer.objects.create(
                user=user,
                name=user.first_name,
                staff_ID=user.userid,
                phone_no=user.phone,
                email=user.email,
                profile_pic=user.profile_pic,
                department=department,
                faculty=faculty,              
                created_by=user4,
        )     
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerlecturer')
        else:
            messages.error(request, "form error")
            return redirect('registerlecturer')
    context = {'form':form}
    return render(request, 'Permissions/registerlecturer.html', context)



@login_required(login_url='login')
@admin_only
def registeradmin(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registeradmin')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registeradmin')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='admin')
            user.groups.add(group)  
            messages.success(request, 'user has been created for ' + name)
            return redirect('registeradmin')
        else:
            messages.error(request, "form error")
            return redirect('registeradmin')
    context = {'form':form}
    return render(request, 'Permissions/registeradmin.html', context)

@login_required(login_url='login')
@admin_only
def registerregistry(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registerregistry')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerregistry')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='registry')
            user.groups.add(group)      
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerregistry')
        else:
            messages.error(request, "form error")
            return redirect('registerregistry')
    context = {'form':form}
    return render(request, 'Permissions/registerregistry.html', context)

@login_required(login_url='login')
@admin_only
def registerbursary(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registerbursary')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerbursary')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='bursary')
            user.groups.add(group)        
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerbursary')
        else:
            messages.error(request, "form error")
            return redirect('registerbursary')
    context = {'form':form}
    return render(request, 'Permissions/registerbursary.html', context)

@login_required(login_url='login')
@admin_only
def registerlibrary(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registerlibrary')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerlibrary')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='library')
            user.groups.add(group)        
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerlibrary')
        else:
            messages.error(request, "form error")
            return redirect('registerlibrary')
    context = {'form':form}
    return render(request, 'Permissions/registerlibrary.html', context)

@login_required(login_url='login')
@admin_only
def registersuperadmin(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registersuperadmin')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registersuperadmin')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='superadmin')
            user.groups.add(group)        
            messages.success(request, 'user has been created for ' + name )
            return redirect('registersuperadmin')
        else:
            messages.error(request, "form error")
            return redirect('registersuperadmin')
    context = {'form':form}
    return render(request, 'Permissions/registersuperadmin.html', context)

@login_required(login_url='login')
@admin_only
def registerhod(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registerhod')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registerhod')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='hod')
            user.groups.add(group)        
            messages.success(request, 'user has been created for ' + name)
            return redirect('registerhod')
        else:
            messages.error(request, "form error")
            return redirect('registerhod')
    context = {'form':form}
    return render(request, 'Permissions/registerhod.html', context)

@login_required(login_url='login')
@admin_only
def registersupervisor(request):
    form = UserForm()
    if request.method =='POST':
        form = UserForm(request.POST)
        userid = request.POST.get('userid')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(userid=userid):
            messages.info(request, "Staff_ID already exists")
            return redirect('registersupervisor')
        if password1 != password2:
            messages.error(request, "Incorrect password")
            return redirect('registersupervisor')
        if form.is_valid():
            user= form.save()
            name = form.cleaned_data.get('first_name')
            group= Group.objects.get(name='supervisor')
            user.groups.add(group)        
            messages.success(request, 'user has been created for ' + name)
            return redirect('registersupervisor')
        else:
            messages.error(request, "form error")
            return redirect('registersupervisor')
    context = {'form':form}
    return render(request, 'Permissions/registersupervisor.html', context)

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_superadmin(user):
    return user.groups.filter(name='superadmin').exists()
def is_student(user):
    return user.groups.filter(name='student').exists()
def is_registry(user):
    return user.groups.filter(name='registry').exists()
def is_bursary(user):
    return user.groups.filter(name='bursary').exists()
def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()
def is_hod(user):
    return user.groups.filter(name='hod').exists()
def is_library(user):
    return user.groups.filter(name='library').exists()
def is_supervisor(user):
    return user.groups.filter(name='supervisor').exists()


def login_user(request):
    if request.method == "POST":
        userid = request.POST['userid']
        password = request.POST['password']
        
        user = authenticate(userid=userid, password=password)

        if user is not None:
            login(request, user)
            return redirect('loginsuccess')     
        else:
            messages.error(request, "Invalid Credientials")
            return redirect('login')

    return render(request, "Permissions/loginpage.html")






@login_required(login_url='login')
@admin_only
def allstudents(request):
    stu= Student.objects.all().order_by('adm_year')
    context={'stu':stu}
    return render(request,'dashboard/allstudents.html',context)


@login_required(login_url='login')
@admin_only
def alllecturers(request):
    lec= Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'dashboard/alllecturers.html',context)


@login_required(login_url='login')
@admin_only
def adminprofile(request):
    user=User.objects.get(id=request.user.id)
    form = UserForm1(instance=user)
    if request.method =='POST':
        form = UserForm1(request.POST, request.FILES,instance=user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'update has been successfully made')
            return redirect('adminprofile')
        else:
            messages.error(request, "form error")
            return redirect('adminprofile')
    context = {'form':form}
    return render(request,'dashboard/adminprofile.html',context)



@login_required(login_url='login')
@admin1_only
def dashboard(request):
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
    return render(request, 'dashboard/dashboard.html',context)



@login_required(login_url='login')
@admin_only
def sentmessage(request):
    user=User.objects.get(id=request.user.id)
    meg=Message.objects.filter(sender=user)
    context={'meg':meg}
    return render(request, 'dashboard/sentmessage.html',context)





@login_required(login_url='login')
@admin_only
def viewmessage(request):
    if is_superadmin(request.user):      
        user1=Group.objects.get(name='superadmin')
        meg= Message.objects.filter(group=user1)
    else:
        user2=Group.objects.get(name='admin')
        meg= Message.objects.filter(group=user2)
    context={'meg':meg}
    return render(request, 'dashboard/viewmessage.html', context)

@login_required(login_url='login')
@admin_only
def template(request):
    form= MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES) 
    context={'form':form}
    return render(request, 'dashboard/template.html', context)

@login_required(login_url='login')
@admin_only
def template1(request):
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
           return redirect('template1') 
        else:
            messages.error(request, 'Message error')
            return redirect('template1') 
    context={'form':form}
    return render(request, 'dashboard/template1.html', context)


@login_required(login_url='login')
@admin_only
def template2(request):
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
           return redirect('template2') 
        else:
            messages.error(request, 'Message error')
            return redirect('template2') 
    context={'form':form}
    return render(request, 'dashboard/template2.html', context)


@login_required(login_url='login')
@admin_only
def template3(request):
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
           return redirect('template3') 
        else:
            messages.error(request, 'Message error')
            return redirect('template3') 
    context={'form':form}
    return render(request, 'dashboard/template3.html', context)


@login_required(login_url='login')
@admin_only
def template4(request):
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
           return redirect('template4') 
        else:
            messages.error(request, 'Message error')
            return redirect('template4') 
    context={'form':form}
    return render(request, 'dashboard/template4.html', context)



@login_required(login_url='login')
@admin_only
def student(request, pk_profile):
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
    return render(request, 'dashboard/studentpage.html', context)



@login_required(login_url='login')
@admin_only
def updatestudent(request, pk):
    stud = Student.objects.get(id=pk)
    user=User.objects.filter(first_name=stud)
    
    form = StudentForm(instance=stud)
    if request.method == 'POST':
       name=request.POST.get('name')
       matric_no=request.POST.get('matric_no')
       phone_no=request.POST.get('phone_no')
       email=request.POST.get('email')
       profile_pic=request.FILES.get('profile_pic')
       form =  StudentForm(request.POST,request.FILES,instance=stud)
       if form.is_valid():
           form.save()
           
           user.update(
                first_name=name,
                userid=matric_no,
                phone=phone_no,
                email=email,
                profile_pic=profile_pic,
                
            )
           messages.success(request, 'updated has been made to ' + name)
           return redirect('student', stud.id)
    context = {'form':form, 'stud':stud}
    return render(request, 'dashboard/updatestudent.html', context)



@login_required(login_url='login')
@admin_only
def regstucourse(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'dashboard/regstucourse.html',context)



@login_required(login_url='login')
@admin_only
def regcourse(request,pk):
    cour=Course.objects.all()
    if not cour:
        messages.info(request, 'No course has been register yet, add a course')
        return redirect('regstucourse')
    stu=Student.objects.get(id=pk)
    form= RegistercourseForm()
    if request.method == 'POST':
       course=Course.objects.get(id=request.POST.get('courseID'))
       cou=Course.objects.filter(name=course)
       cu=cou[0].course_unit
       sem=cou[0].semester
       form =  RegistercourseForm(request.POST)
       if form.is_valid():
           form=form.save(commit=False)
           form.course=course
           form.student=stu
           form.semester=sem
           form.course_unit=cu
           form.save()
           messages.success(request, 'course has been register for ' + str(stu))
           return redirect('regcourse',stu.id)
       else:
           messages.error(request, 'Form error')
           return redirect('regcourse',stu.id)
    context={'form':form}
    return render(request, 'dashboard/regcourse.html', context)



@login_required(login_url='login')
@admin_only
def stucourse(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'dashboard/stucourse.html', context)



@login_required(login_url='login')
@admin_only
def coursestudent(request, pk):
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
        total=cou.aggregate(Sum('course_unit'))['course_unit__sum']
        total1=cou1.aggregate(Sum('course_unit'))['course_unit__sum']
        total2=cou2.aggregate(Sum('course_unit'))['course_unit__sum']
        total3=cou3.aggregate(Sum('course_unit'))['course_unit__sum']
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
    else:
        messages.info(request, 'Student has not Registered any course yet')
        return redirect('stucourse')
    if not cou or cou1 or cou2 or cou3:
        messages.info(request, 'Student has not Registered any course yet')
        return redirect('stucourse')
    context={'cou':cou,'cou1':cou1,'cou2':cou2,'cou3':cou3,
             'tit':tit,'tit1':tit1,'tit2':tit2,'tit3':tit3,'stu':stu,
             'total':total,'total1':total1,'total2':total2,
             'total3':total3}
    return render(request, 'dashboard/coursestudent.html', context)



@login_required(login_url='login')
@admin_only
def makepayment(request):
    form= FileForm()
    if request.method == 'POST':
       form =  FileForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('dashboard') 
    context={'form':form}
    return render(request, 'dashboard/makepayment.html', context)


@login_required(login_url='login')
@admin_only
def creditpayment(request):
    user=User.objects.get(id=request.user.id)
    form= CreditForm()
    if request.method == 'POST':
        name=request.POST.get('studentID')
        form =  CreditForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            student=Student.objects.get(id=request.POST.get('studentID'))
            print(student)
            stu=Student.objects.filter(name=student)
            dep=stu[0].department
            schoollevy=Schoollevy.objects.get(id=request.POST.get('schoollevyID'))
            form.student=student
            form.schoollevy=schoollevy
            form.department=dep
            form.user=user
            if form.credit == 0:
                messages.error(request, 'you have inputted a wrong value')
                return redirect('creditpayment')
            else:
                form.save()
                messages.success(request, 'student has been Credited successfully')
                return redirect('creditpayment')
    context={'form':form}
    return render(request, 'dashboard/creditpayment.html', context)



@login_required(login_url='login')
@admin_only
def debitpayment(request):
    user=User.objects.get(id=request.user.id)
    form= DebitForm()
    if request.method == 'POST':
        name=request.POST.get('studentID')
        form =  DebitForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            student=Student.objects.get(id=request.POST.get('studentID'))
            print(student)
            stu=Student.objects.filter(name=student)
            dep=stu[0].department
            schoollevy=Schoollevy.objects.get(id=request.POST.get('schoollevyID'))
            form.student=student
            form.schoollevy=schoollevy
            form.department=dep
            form.user=user
            if form.debit == 0:
                messages.error(request, 'you have inputted a wrong value')
                return redirect('debitpayment')
            tra=Transaction.objects.filter(student=student,schoollevy=schoollevy)
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
            bal=total_credit - (total_paid + form.debit)
            if bal <= -1:
                messages.error(request, 'you are inputting the wrong value')
                return redirect('debitpayment')
            else:
                form.save()
                messages.success(request, 'student has been debited successfully')
                return redirect('debitpayment') 
    context={'form':form}
    return render(request, 'dashboard/debitpayment.html', context)




@login_required(login_url='login')
@admin_only
def transactions(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'dashboard/transactions.html', context)


@login_required(login_url='login')
@admin_only
def summary(request,pk):
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
    return render(request, 'dashboard/summary.html', context=mydict)




@login_required(login_url='login')
@admin_only
def receipt(request,pk):
    tra=Transaction.objects.get(id=pk)
    context={'tra':tra}
    return render(request, 'dashboard/receipt.html', context)



@login_required(login_url='login')
@admin_only
def resettable(request):
    context={}
    return render(request, 'dashboard/resettable.html', context)


@login_required(login_url='login')
@admin_only
def resettab(request):
    Timetable.objects.all().delete()
    messages.success(request, ' Timetable has been successfully reset')
    return redirect('resettable')


@login_required(login_url='login')
@admin_only
def admintable(request):
    tim=Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'dashboard/admintable.html', context)


@login_required(login_url='login')
@admin_only
def adminexamtable(request):
    tim=Exam_Timetable.objects.filter(week='Monday').order_by('timefrom')
    tim1=Exam_Timetable.objects.filter(week='Tuesday').order_by('timefrom')
    tim2=Exam_Timetable.objects.filter(week='Wednesday').order_by('timefrom')
    tim3=Exam_Timetable.objects.filter(week='Thursday').order_by('timefrom')
    tim4=Exam_Timetable.objects.filter(week='Friday').order_by('timefrom')
    context={'tim':tim,'tim1':tim1,'tim2':tim2,'tim3':tim3,'tim4':tim4}
    return render(request, 'dashboard/adminexamtable.html', context)


@login_required(login_url='login')
@admin_only
def resetexam(request):
    Exam_Timetable.objects.all().delete()
    messages.success(request, 'Exam table has been successfully reset')
    return redirect('resettable')


@login_required(login_url='login')
@admin_only
def viewtransaction(request, pk):
    levy=Schoollevy.objects.get(id=pk)
    tra=Transaction.objects.filter(schoollevy=levy)
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
    
    context={'tra':tra,'total_paid':total_paid,'total_credit':total_credit,'bal':bal}
    return render(request, 'dashboard/viewtransaction.html', context)








@login_required(login_url='login')
@admin_only
def uploadfile(request):
    form= FileForm()
    if request.method == 'POST':
        student=request.POST.get('student')
        title=request.POST.get('title')
        if File.objects.filter(title=title, student=student):
            messages.info(request, 'file already existed for ' + str(student) )
            return redirect('uploadfile')
        form =  FileForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            student=Student.objects.get(id=request.POST.get('studentID'))
            form.student=student
            form.save()
            messages.success(request, 'file has been uploaded for ' + str(student) )
            return redirect('uploadfile') 
        else:
            messages.error(request, 'form error')
            return redirect('uploadfile') 
    context={'form':form}
    return render(request, 'dashboard/uploadfile.html', context)



@login_required(login_url='login')
@admin_only
def lecturer(request, pk_profile1):
    lec=Lecturer.objects.get(id=pk_profile1)
    fil=File2.objects.filter(lecturer=pk_profile1)
    work=Work_Experience1.objects.filter(lecturer=pk_profile1)
    ins=Institution_Attended1.objects.filter(lecturer=pk_profile1)
    sta=Status.objects.filter(user=lec)
    cou=Course.objects.filter(lecturer=lec)
    context={'lec':lec, 'item':lec,'fil':fil,'work':work,
             'ins':ins,'sta':sta,'cou':cou}
    return render(request, 'dashboard/lecturer.html', context)




@login_required(login_url='login')
@admin_only
def updatelecturer(request, pk1):
    lect = Lecturer.objects.get(id=pk1)
    user=User.objects.get(first_name=lect)
    lecturer = Lecturer.objects.filter(user=user)
    print(lecturer)
    form = LecturerForm(instance=user)
    if request.method == 'POST':
       name=request.POST.get('name')
       faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
       department=Department.objects.get(id=request.POST.get('departmentID'))

       form =  LecturerForm(request.POST,request.FILES, instance=user)
       if form.is_valid():
           form.save()
           
           lecturer.update(
                user=user,
                name=user.first_name,
                staff_ID=user.userid,
                phone_no=user.phone,
                email=user.email,
                profile_pic=user.profile_pic,
                department=department,
                faculty=faculty
                )
           messages.success(request,'update was updated successfully')
           return redirect('lecturer', lect.id)
       else:
           messages.error(request, 'form error')
           return redirect('updatelecturer', lect.id)
    context = {'form':form, 'lect':lect}
    return render(request, 'dashboard/updatelecturer.html', context)


@login_required(login_url='login')
@admin_only
def lecturerview(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request, 'dashboard/lecturerview.html', context)


@login_required(login_url='login')
@admin_only
def lectureresult(request,pk):
    lec=Lecturer.objects.get(id=pk)
    res=LecturerResult.objects.filter(lecturer=lec).order_by('date')
    if not res:
        messages.info(request, 'Lecturer has not submitted any student result yet')
        return redirect(lecturerview)
    context={'res':res}
    return render(request, 'dashboard/lectureresult.html', context)



@login_required(login_url='login')
@admin_only
def newfaculty(request):
    form= FacultyForm()
    user1=User.objects.get(id=request.user.id)
    user=User.objects.filter(id=request.user.id)
    token1=user[0].token
    if request.method == 'POST':
        form= FacultyForm(request.POST)
        name = request.POST.get('name')
        token=request.POST.get('token')
        if token1 != token:
            messages.error(request, "Invalid Token Submitted")
            return redirect('newfaculty')
        if Faculty.objects.filter(name=name):
            messages.info(request, "Faculty Already Exit")
            return redirect('newfaculty')
        if form.is_valid():
            form=form.save(commit=False)
            form.created_by=user1
            form.save()
            messages.success(request, name + ' has been added to faculty list')
            return redirect('newfaculty')
        else:
            messages.success(request, 'form error')
            return redirect('newfaculty')
    context= {'form':form}    
    return render(request, 'dashboard/newfaculty.html', context)





@login_required(login_url='login')
@admin_only
def faculty(request, pk_profile2):
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
    return render(request, 'dashboard/facultypage.html', context)


@login_required(login_url='login')
@admin_only
def updatefaculty(request, pk):
    facu = Faculty.objects.get(id=pk)
    form = FacultyForm1(instance=facu)
    if request.method == 'POST':
        name=request.POST.get('name')
        form =  FacultyForm1(request.POST,instance=facu)
        if form.is_valid():
           form.save()
           messages.success(request, name + ' has been updated successfully')
           return redirect('faculty', facu.id)
        else:
           messages.error(request, ' form error')
           return redirect('updatefaculty', facu.id)
    context={'form':form}
    return render(request, 'dashboard/updatefaculty.html', context)



@login_required(login_url='login')
@admin_only
def updatedepartment(request, pk):
    depu=Department.objects.get(id=pk)
    form = DepartmentForm1(instance=depu)
    if request.method == 'POST':
       name=request.POST.get('name')
       form =  DepartmentForm1(request.POST,instance=depu)
       if form.is_valid():
           form.save()
           messages.success(request, name + ' has been updated successfully')
           return redirect('department', depu.id)
       else:
           messages.error(request, ' form error')
           return redirect('updatedepartment', depu.id)
    context={'form':form}
    return render(request, 'dashboard/updatedepartment.html', context)


@login_required(login_url='login')
@admin_only
def newdepartment(request):
    form= DepartmentForm()
    user1=User.objects.get(id=request.user.id)
    user=User.objects.filter(id=request.user.id)
    token1=user[0].token
    if request.method == 'POST':
        form= DepartmentForm(request.POST)
        name = request.POST.get('name')
        token=request.POST.get('token')
        if token1 != token:
            messages.error(request, "Invalid Token Submitted")
            return redirect('newdepartment')
        form= DepartmentForm(request.POST)
        if Department.objects.filter(name=name):
            messages.info(request, "Department Already Exit")
            return redirect('newdepartment')
        if form.is_valid():
            form=form.save(commit=False)
            faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
            form.faculty=faculty
            form.created_by=user1
            form.save()
            
            messages.success(request, name + ' has been added to Department list')
            return redirect('newdepartment')
        else:
            messages.success(request, 'form error')
            return redirect('newdepartment')
    context= {'form':form}   
    return render(request, 'dashboard/newdepartment.html', context)





@login_required(login_url='login')
@admin_only
def department(request, pk_profile3):
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
    return render(request, 'dashboard/department.html', context)




@login_required(login_url='login')
@admin_only
def newcourse(request):
    user1=User.objects.get(id=request.user.id)
    user=User.objects.filter(id=request.user.id)
    token1=user[0].token
    form=CourseForm1()
    if request.method == 'POST':
        name = request.POST.get('name')
        token=request.POST.get('token')
        if token1 != token:
            messages.error(request, "Invalid Token Submitted")
            return redirect('newcourse')
        if Course.objects.filter(name=name):
            messages.info(request, 'Course with this name already existed')
            return redirect(newcourse)
        form= CourseForm1(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            lecturer=Lecturer.objects.get(id=request.POST.get('lecturerID'))
            faculty=Faculty.objects.get(id=request.POST.get('facultyID'))
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.lecturer=lecturer
            form.faculty=faculty
            form.department=department
            form.created_by=user1
            form.save()
            messages.success(request, name + ' has been successfully added')
            return redirect('newcourse')
        else:
            messages.success(request, 'form error')
            return redirect('newcourse')
    context= {'form':form}   
    return render(request, 'dashboard/newcourse.html', context)


@login_required(login_url='login')
@admin_only
def adminviewcourse(request):
    dep=Department.objects.all()
    context={'dep':dep}
    return render(request, 'dashboard/adminviewcourse.html', context)


@login_required(login_url='login')
@admin_only
def viewresult(request):
    stu=Student.objects.all()
    context={'stu':stu}
    return render(request, 'dashboard/viewresult.html', context)


@login_required(login_url='login')
@admin_only
def adminsturesult(request, pk):
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
        cgpa=(gpa+gpa1) / 2   
    
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
        cgpa2=(gpa2+gpa3) /2
        
    if cgpa==0 or cgpa2==0:
        messages.info(request, ' Total cgpa will not be calculated, invalid input')
        cgpa1=0
    else:
        cgpa1=(cgpa+cgpa2) /2
        
        
        
        
        
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
    return render(request, 'dashboard/adminsturesult.html', context)


@login_required(login_url='login')
@admin_only
def deleteresult(request,pk):
    res=Result.objects.filter(id=pk)
    res.delete()
    messages.success(request, 'Result has been deleted successfully')
    return redirect('viewresult')



@login_required(login_url='login')
@admin_only
def viewcourse(request,pk):
    dep=Department.objects.get(id=pk)
    cou=Course.objects.filter(department=dep)
    if not cou:
        messages.info(request, 'there is no course in this department yet')
        return redirect('adminviewcourse')
    
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
    return render(request, 'dashboard/viewcourse.html', context)


@login_required(login_url='login')
@admin_only
def updatecourse(request,pk):
    dep1=Course.objects.get(id=pk)
    form=CourseForm2(instance=dep1)
    if request.method == 'POST':
        name=request.POST.get('name')
        form= CourseForm2(request.POST, instance=dep1)
        if form.is_valid():
            form.save()
            messages.success(request, name + ' has been updated successfully')
            return redirect('updatecourse', dep1.id)
        else:
            messages.error(request, 'Update error')
            return redirect('updatecourse', dep1.id)
    context= {'form':form}   
    return render(request, 'dashboard/updatecourse.html', context)






@login_required(login_url='login')
@admin_only
def newstudentlevy(request):
    form=LevyForm()
    if request.method == 'POST':
        name=request.POST.get('name')
        if Schoollevy.objects.filter(name=name):
            messages.info(request, name + ' Levy already added to the list')
            return redirect('newstudentlevy')
        form= LevyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, name + ' Levy added successfully')
            return redirect('newstudentlevy')
        else:
            messages.error(request, 'form error')
            return redirect('newstudentlevy')
    context= {'form':form}   
    return render(request, 'dashboard/newstudentlevy.html', context)



@login_required(login_url='login')
@admin_only
def result(request):
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
            return redirect('result')
        else:
            messages.error(request, 'form error')
            return redirect('result')
    context= {'form':form}   
    return render(request, 'dashboard/result.html', context)

@login_required(login_url='login')
@admin_only
def viewfaculty(request):
    fac=Faculty.objects.all()
    context = {'fac':fac}
    return render(request, 'dashboard/viewfaculty.html', context)



@login_required(login_url='login')
@admin_only
def viewdepartment(request):
    dep=Department.objects.all()
    context = {'dep':dep}
    return render(request,'dashboard/viewdepartment.html',context)




@login_required(login_url='login')
@admin_only
def settimetable(request):
    form= TableForm()
    if request.method == 'POST':
        course=Course.objects.get(id=request.POST.get('courseID'))
        lec=Course.objects.filter(name=course)
        lecturer=lec[0].lecturer
        form= TableForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.course=course
            form.department=department
            form.lecturer=lecturer
            form.save()
            messages.success(request, 'successfully addded to timetable')
            return redirect('settimetable')
        else:
            messages.error(request, 'form error')
            return redirect('settimetable')
    context= {'form':form}  
    return render(request,'dashboard/settimetable.html',context)


@login_required(login_url='login')
@admin_only
def setexamtable(request):
    form= ExamTableForm()
    if request.method == 'POST':
        form= ExamTableForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            department=Department.objects.get(id=request.POST.get('departmentID'))
            form.course=course
            form.department=department
            form.save()
            messages.success(request, 'successfully addded to Exam timetable')
            return redirect('setexamtable')
        else:
            messages.error(request, 'form error')
            return redirect('setexamtable')
    context= {'form':form}  
    return render(request,'dashboard/setexamtable.html',context)



@login_required(login_url='login')
@admin_only
def addquestion(request):
    lec=User.objects.get(id=request.user.id)
    questionForm=QuestionForm()
    if request.method=='POST':
        question=request.POST.get('question')
        if Question.objects.filter(question=question):
            messages.info(request, "Question has been submitted already")
            return redirect('addquestion') 
        questionForm=QuestionForm(request.POST)
        if questionForm.is_valid():
            question=questionForm.save(commit=False)
            course=Course.objects.get(id=request.POST.get('courseID'))
            question.course=course
            question.user=lec
            question.save()
            messages.success(request, "Question has been added")
            return redirect('addquestion')   
        else:
            messages.error(request, "form is invalid")
            return redirect('addquestion')      
    context={'questionForm':questionForm}
    return render(request,'dashboard/addquestion.html',context)


@login_required(login_url='login')
@admin_only
def viewquestion(request):
    cou=Course.objects.all()
    return render(request,'dashboard/viewquestion.html',{'cou':cou})

@login_required(login_url='login')
@admin_only
def viewquestionview(request,pk):
    course=Course.objects.get(id=pk)
    que=Question.objects.filter(course=course)
    if not que:
        messages.info(request, 'There is no Question for this Course yet!!!!!')
        return redirect('viewquestion')
    p=Paginator(que, 1)
    page_num = request.GET.get('page',1)
    try:
        page = p.page(page_num)
    except EmptyPage:
            page = p.page(1)
    context={'que':page}
    return render(request,'dashboard/viewquestionview.html',context)

@login_required(login_url='login')
@admin_only
def deletequestion(request,pk):
    que=Question.objects.filter(id=pk)
    que.delete()
    messages.success(request, 'Questions has been deleted successfully')
    return redirect('viewquestion')

@login_required(login_url='login')
@admin_only
def studentmark(request):
    stu= Student.objects.all()
    context={'stu':stu}
    return render(request,'dashboard/studentmark.html',context)

@login_required(login_url='login')
@admin_only
def marks(request,pk):
    stu=Student.objects.get(id=pk)
    res=Result1.objects.filter(student=stu)
    cou =Course.objects.filter(result1__student=stu)
    if not cou:
        messages.info(request, 'There is no exam result for this student yet')
        return redirect('studentmark')
    context={'cou':cou}
    response =  render(request,'dashboard/marks.html',context)
    response.set_cookie('student_id',str(pk))
    return response

@login_required(login_url='login')
@admin_only
def checkmarks(request,pk):
    course =Course.objects.get(id=pk)
    questions=Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    student_id = request.COOKIES.get('student_id')
    student= Student.objects.get(id=student_id)
    res= Result1.objects.all().filter(course=course).filter(student=student)
    context={'res':res,'total_marks':total_marks}
    return render(request,'dashboard/checkmarks.html',context)


@login_required(login_url='login')
@admin_only
def deletemark(request, pk):
    user =User.objects.get(id=request.user.id)
    res= Result1.objects.get(id=pk)
    res.delete()
    messages.success(request, 'student mark has been deleted successfully')
    return redirect('studentmark')
    
@login_required(login_url='login')
@admin_only   
    
def newnotice(request):
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
            return redirect('newnotice')
        else:
            messages.error(request, 'form error')
            return redirect('newnotice')
    context={'form':form}
    return render(request,'dashboard/newnotice.html',context)


@login_required(login_url='login')
@admin_only
def newnotice1(request):
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
            return redirect('newnotice1')
        else:
            messages.error(request, 'form error')
            return redirect('newnotice1')
    context={'form':form}
    return render(request,'dashboard/newnotice1.html',context)


@login_required(login_url='login')
@admin_only
def noticeboard(request):
    context={}
    return render(request,'dashboard/noticeboard.html',context)


@login_required(login_url='login')
@admin_only
def departmentnotice(request):
    notice=DepartmentNotice.objects.all()
    context={'notice':notice}
    return render(request,'dashboard/departmentnotice.html',context)


@login_required(login_url='login')
@admin_only
def generalnotice(request):
    notice=Notice.objects.all().order_by('date')
    context={'notice':notice}
    return render(request,'dashboard/generalnotice.html',context)



@login_required(login_url='login')
@admin_only
def deletedepnotice(request):
    notice=DepartmentNotice.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('departmentnotice')


@login_required(login_url='login')
@admin_only
def deletenotice(request,pk):
    notice=Notice.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('generalnotice')



@login_required(login_url='login')
@admin_only
def deletemessage(request,pk):
    notice=Message.objects.get(id=pk)
    notice.delete()
    messages.success(request, 'Deleted successfully')
    return redirect('sentmessage')


@login_required(login_url='login')
@admin_only
def viewbook(request):
    books=LMODEL.Book.objects.all()
    context={'books':books}
    return render(request,'dashboard/viewbook.html',context)



@login_required(login_url='login')
@admin_only
def studentlib(request):
    students=LMODEL.Student.objects.all()
    context={'students':students}
    return render(request,'dashboard/studentlib.html',context)



@login_required(login_url='login')
@admin_only
def issuedlibook(request):
    issuedbooks=LMODEL.IssuedBook.objects.all()
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


        books=list(LMODEL.Book.objects.filter(isbn=ib.isbn))
        students=list(LMODEL.Student.objects.filter(department=ib.department))
        i=0
        for l in books:
            t=(students[i].name,students[i].department,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)
    messages.info(request, 'Fine will be given to student after 15days of issued books')
    context={'li':li}
    return render(request,'dashboard/issuedlibook.html',context)



@login_required(login_url='login')
@admin_only
def attendance(request):
    att=Attendance.objects.all().order_by('date')
    context={'att':att}
    return render(request,'dashboard/attendance.html',context)


@login_required(login_url='login')
@admin_only
def examrecord(request):
    exam=VMODEL.Examination.objects.all()
    context={'exam':exam}
    return render(request,'dashboard/examrecord.html',context)



@login_required(login_url='login')
@admin_only
def malpracticeview(request):
    mal=VMODEL.Malpractice.objects.all()
    context={'mal':mal}
    return render(request,'dashboard/malpractice.html',context)



@login_required(login_url='login')
@admin_only
def deletemalpractice(request,pk):
    mal=VMODEL.Malpractice.objects.get(id=pk)
    mal.delete()
    messages.success(request, 'deletion was successful')
    return redirect('malpracticeview')



@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['superadmin'])
def payroll(request):
  
    return render(request,'dashboard/payroll.html')

@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['superadmin'])
def staffpayroll(request):
    pay=Staff_Payroll.objects.all()
    t_price=pay.aggregate(Sum('r_sal'))['r_sal__sum']
    if t_price==0:
        t_price = 0
    context={'pay':pay,'t_price':t_price}
    return render(request,'dashboard/staffpayroll.html',context)


@login_required(login_url='login')

def deletestaffpayroll(request,pk):
    sta=Staff_Payroll.objects.get(id=pk)
    sta.delete()
    messages.success(request, 'Staff has been removed from payroll')
    return redirect('staffpayroll')



@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['superadmin'])
def lecturerpayroll(request):
    lec=Lecturer.objects.all()
    context={'lec':lec}
    return render(request,'dashboard/lecturerpayroll.html',context)



@login_required(login_url='login')
@admin_only
@allowed_users(allowed_roles=['superadmin'])
def lecpay(request, pk):
    lec=Lecturer.objects.get(id=pk)
    res=Course.objects.filter(lecturer=lec)
    t_price=res.aggregate(Sum('price'))['price__sum']
    if t_price==0:
        t_price = 0
    context={'res':res,'t_price':t_price}
    return render(request,'dashboard/lecpay.html',context)


@login_required(login_url='login')
@admin_only
def addpayroll(request):
    form=PayrollForm()
    if request.method=='POST':
        staff=request.POST.get('staff')
        form=PayrollForm(request.POST)
        if form.is_valid():
            if Staff_Payroll.objects.filter(staff=staff):
                messages.info(request, staff + ' Already on the list')
                return redirect('addpayroll')
            form.save()
            messages.success(request, staff + 'has been added successfully')
            return redirect('addpayroll')
        else:
            messages.error(request, 'form error')
            return redirect('addpayroll')
    context={'form':form}
    return render(request,'dashboard/addpayroll.html',context)


@login_required(login_url='login')
@admin_only
def status(request):
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
                return redirect('status')
            form.save()
            messages.success(request, 'Status has been uploaded')
            return redirect('status')
        else:
            messages.error(request, 'form error')
            return redirect('status')
    context={'form':form}
    return render(request,'dashboard/status.html',context)


@login_required(login_url='login')
@admin_only
def deletestatus(request):
    user=User.objects.get(id=request.user.id)
    sta=Status.objects.filter(user=user)
    sta.delete()
    messages.success(request, 'Status has been Deleted')
    return redirect('viewstatus')



@login_required(login_url='login')
@admin_only
def viewstatus(request):
    
    sta=Status.objects.all().order_by('expiry')
    context={'sta':sta}
    return render(request,'dashboard/viewstatus.html',context)


@login_required(login_url='login')
@admin_only
def addcalendar(request):
    form=EventForm()
    if request.method=='POST':
        form=EventForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.save()
            messages.success(request, 'Event has been added to calendar')
            return redirect('addcalendar')
        else:
            messages.error(request, 'form error')
            return redirect('addcalendar')
    context= {'form':form}
    return render(request, 'dashboard/addcalendar.html', context)


@login_required(login_url='login')
@admin_only
def resetcalendar(request):

    return render(request, 'dashboard/addcalendar.html', context)



class CalendarView(generic.ListView):
    model = Event
    template_name = 'dashboard/calendar.html'
 
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