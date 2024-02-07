from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from administrator import models as QMODEL
from administrator import filters as QFILTER
from django.contrib import messages
from django.db.models import Sum




def allow_login(view_func):
    def wrapper_function(request, *args, **kwargs):
        accountapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,access=True)
        accountdisapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,access=False)
        if accountdisapproval:
            return redirect("accesslogout1")
        elif accountapproval:
            return view_func(request, *args,**kwargs)
    return wrapper_function


def admissionstatus(view_func):
    def wrapper_function(request, *args, **kwargs):
        accountapproval=QMODEL.Student.objects.all().filter(user_id=request.user.id,adminstatus=False)
        if accountapproval:
            messages.info(request, 'Your Admission has not been granted yet, so therefore you cannot view this page. ')
            return redirect("studentdashboard")
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function


def allow_exam(view_func):
    def wrapper_function(request, *args, **kwargs):
        noaccess=QMODEL.Student.objects.all().filter(user_id=request.user.id,examaccess=False)
        access=QMODEL.Student.objects.all().filter(user_id=request.user.id,examaccess=True)
        if noaccess:
            messages.info(request, "You don't have access to view this page, You have balance your tuition fees")
            return redirect('studentdashboard')
        elif access:
            return view_func(request, *args,**kwargs)
    return wrapper_function



def exam_entry(view_func):
    def wrapper_function(request, *args, **kwargs):
        stu=QMODEL.Student.objects.get(user_id=request.user.id)
        sch=QMODEL.Schoollevy.objects.get(name__startswith='tuit')
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
            messages.info(request, 'you havent balance  your tuitution fee')
            return redirect('studentdashboard')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function




def library_entry(view_func):
    def wrapper_function(request, *args, **kwargs):
        stu=QMODEL.Student.objects.get(user_id=request.user.id)
        sch=QMODEL.Schoollevy.objects.get(name__startswith='libr')
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
            messages.info(request, 'you havent balance  your Library fee')
            return redirect('studentdashboard')
        else:
            return view_func(request, *args,**kwargs)
    return wrapper_function



def allow_result(view_func):
    def wrapper_function(request, *args, **kwargs):
        noaccess=QMODEL.Student.objects.all().filter(user_id=request.user.id,resultaccess=False)
        access=QMODEL.Student.objects.all().filter(user_id=request.user.id,resultaccess=True)
        if noaccess:
            messages.info(request, "You don't have access to view this page, You have balance your tuition fees")
            return redirect('studentdashboard')
        elif access:
            return view_func(request, *args,**kwargs)
    return wrapper_function
