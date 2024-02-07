from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from administrator import models as QMODEL
  
            

def allow_user(view_func):
    def wrapper_function(request, *args, **kwargs):
        accountapproval=QMODEL.Lecturer.objects.all().filter(user_id=request.user.id,access=True)
        accountdisapproval=QMODEL.Lecturer.objects.all().filter(user_id=request.user.id,access=False)
        if accountdisapproval:
            return redirect("accesslogout")
        elif accountapproval:
            return view_func(request, *args,**kwargs)
    return wrapper_function



def exam_entry(view_func):
    def wrapper_function(request, *args, **kwargs):
        accountapproval=QMODEL.Lecturer.objects.all().filter(user_id=request.user.id,examaccess=True)
        accountdisapproval=QMODEL.Lecturer.objects.all().filter(user_id=request.user.id,examaccess=False)
        if accountdisapproval:
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif accountapproval:
            return view_func(request, *args,**kwargs)
    return wrapper_function