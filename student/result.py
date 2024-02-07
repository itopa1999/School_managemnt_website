from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
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
@admissionstatus
@student_only
@allow_login
@allow_result
def sturesult(request):
    user=User.objects.filter(id=request.user.id)
    token=user[0].token
    if request.method=='POST':
        token1=request.POST['token']
        if token != token1:
            messages.error(request, 'Invalid token submitted')
            return redirect('sturesult')
        else:
            student =QMODEL.Student.objects.get(user_id=request.user.id)
            tra=QMODEL.Transaction.objects.filter(student=student)
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
            if bal > 0:
                messages.error(request, 'you are not cleared')
                return redirect('noaccess1')
            stu=QMODEL.Student.objects.filter(user_id=request.user.id)
            dep=stu[0].department
            student =QMODEL.Student.objects.get(user_id=request.user.id)
            re=QMODEL.Result.objects.filter(student=student)
            ndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="ND")
            hndstudent =QMODEL.Student.objects.filter(user_id=request.user.id,level="HND")
            if ndstudent:
                res=re.filter(course__semester="ND1 first Semester",course__department=dep)
                res1=re.filter(course__semester="ND1 second Semester",course__department=dep)
                res2=re.filter(course__semester="ND2 first Semester",course__department=dep)
                res3=re.filter(course__semester="ND2 second Semester",course__department=dep)
                t="ND1 FIRST SEMESTER"
                t1="ND1 SECOND SEMESTER"
                t2="ND2 FIRST SEMESTER"
                t3="ND2 SECOND SEMESTER"
                tit="ND1 SEMESTER"
                tit1="ND2 SEMESTER"
            elif hndstudent:
                res=re.filter(course__semester="HND1 first Semester",course__department=dep)
                res1=re.filter(course__semester="HND1 second Semester",course__department=dep)
                res2=re.filter(course__semester="HND2 first Semester",course__department=dep)
                res3=re.filter(course__semester="HND2 second Semester",course__department=dep)
                t="HND1 FIRST SEMESTER"
                t1="HND1 SECOND SEMESTER"
                t2="HND2 FIRST SEMESTER"
                t3="HND2 SECOND SEMESTER"
                tit="HND1 SEMESTER"
                tit1="HND2 SEMESTER"
            else:
                messages.error(request, 'This form must be filled before accessing some features')
                return redirect('form')
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
            if gpa and gpa1 !=0:
                cgpa=(gpa+gpa1) / 2  
            else:
                cgpa=0
            if qp2  is None and cu2 is None:
                gpa2=0
            else:
                gpa2=qp2/cu2
            if qp3  is None and cu3 is None:
                gpa3=0
            else:
                gpa3=qp3/cu3
            if gpa2 and gpa3 !=0:
                cgpa2=(gpa2+gpa3) /2
            else:
                cgpa1=0
            if cgpa and cgpa1 !=0:
                cgpa2=(cgpa+cgpa2) /2
            else:
                cgpa2=0
            
            
            
            if gpa >=3.50:
                gra=("DISTINCTION")
            elif gpa <=3.49 and gpa >=3.00:
                gra =("UPPER CREDIT")
            elif gpa <=2.99 and gpa >=2.50:
                gra =("LOWER CREDIT")
            elif gpa <=2.49 and gpa >=2.00:
                gra =("PASS")
            elif gpa <=1.99 and gpa >=0.01:
                gra =("FAIL")
            else:
                gra =''
            
            
            
            
            if gpa1 >=3.50:
                gra1=("DISTINCTION")
            elif gpa1 <=3.49 and gpa1 >=3.00:
                gra1 =("UPPER CREDIT")
            elif gpa1 <=2.99 and gpa1 >=2.50:
                gra1 =("LOWER CREDIT")
            elif gpa1 <=2.49 and gpa1 >=2.00:
                gra1 =("PASS")
            elif gpa1 <=1.99 and gpa1 >=0.01:
                gra1 =("FAIL")
            else:
                gra1 =''
                
                
            if gpa2 >=3.50:
                gra2=("DISTINCTION")
            elif gpa2 <=3.49 and gpa2 >=3.00:
                gra2 =("UPPER CREDIT")
            elif gpa2 <=2.99 and gpa2 >=2.50:
                gra2 =("LOWER CREDIT")
            elif gpa2 <=2.49 and gpa2 >=2.00:
                gra2 =("PASS")
            elif gpa2 <=1.99 and gpa2 >=0.01:
                gra2 =("FAIL")
            else:
                gra2 =''
                
                
                
            if gpa3 >=3.50:
                gra3=("DISTINCTION")
            elif gpa3 <=3.49 and gpa3 >=3.00:
                gra3 =("UPPER CREDIT")
            elif gpa3 <=2.99 and gpa3 >=2.50:
                gra3 =("LOWER CREDIT")
            elif gpa3 <=2.49 and gpa3 >=2.00:
                gra3 =("PASS")
            elif gpa3 <=1.99 and gpa3 >=0.01:
                gra3 =("FAIL")
            else:
                gra3 =''
            
            
            
                
                
                
            if cgpa >=3.50:
                grade=("DISTINCTION")
            elif cgpa <=3.49 and cgpa >=3.00:
                grade =("UPPER CREDIT")
            elif cgpa <=2.99 and cgpa >=2.50:
                grade =("LOWER CREDIT")
            elif cgpa <=2.49 and cgpa >=2.00:
                grade =("PASS")
            elif cgpa <=1.99 and cgpa >=0.01:
                grade =("FAIL")
            else:
                grade =''
                
                
            if cgpa1 >=3.50:
                grade1=("DISTINCTION")
            elif cgpa1 <=3.49 and cgpa1 >=3.00:
                grade1 =("UPPER CREDIT")
            elif cgpa1 <=2.99 and cgpa1 >=2.50:
                grade1 =("LOWER CREDIT")
            elif cgpa1 <=2.49 and cgpa1 >=2.00:
                grade1 =("PASS")
            elif cgpa1 <=1.99 and cgpa1 >=0.01:
                grade1 =("FAIL")
            else:
                grade1 =''
                
            if cgpa2 >=3.50:
                grade2=("DISTINCTION")
            elif cgpa2 <=3.49 and cgpa2 >=3.00:
                grade2 =("UPPER CREDIT")
            elif cgpa2 <=2.99 and cgpa2 >=2.50:
                grade2 =("LOWER CREDIT")
            elif cgpa2 <=2.49 and cgpa2 >=2.00:
                grade2 =("PASS")
            elif cgpa2 <=1.99 and cgpa2 >=0.01:
                grade2 =("FAIL")
            else:
                grade2 =''
            context={'cgpa':cgpa,'cgpa1':cgpa1,'cgpa2':cgpa2,'tit':tit,'tit1':tit1,'grade':grade,
                    'grade1':grade1,'grade2':grade2,'gpa':gpa,'gpa':gpa1,'gpa1':gpa,'gpa2':gpa2,
                    'gpa3':gpa3,'t':t,'t1':t1,'t2':t2,'t3':t3,'gra':gra,'gra1':gra1,'gra2':gra2,
                    'gra3':gra3,}
            return render(request,'student/studentresult.html',context)
    context={}
    return render(request,'student/sturesult.html',context)

