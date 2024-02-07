from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            group= None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func(request, *args,**kwargs)
            else:
                messages.info(request, "You don't have access to view this page, only super-admin")
                return redirect('dashboard')
        return wrapper_func
    return decorator



def admin1_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            return redirect('logout')
        elif group == 'registry':
            return redirect('registrydashboard')
        elif group == 'library':
            return redirect('librarydashboard')
        elif group == 'supervisor':
            return redirect('supervisordashboard')
        elif group == 'bursary':
            return redirect('bursarydashboard')
        elif group == 'lecturer':
            return redirect('lecturerdashboard')
        elif group == 'hod':
            return redirect('hoddashboard')
        if group == 'admin':
            return view_func(request, *args,**kwargs)
        if group == 'superadmin':
            return view_func(request, *args,**kwargs)
    return wrapper_function



def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'hod':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('hoddashboard')
        if group == 'admin':
            return view_func(request, *args,**kwargs)
        if group == 'superadmin':
            return view_func(request, *args,**kwargs)
    return wrapper_function
    
    

def student_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'hod':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('hoddashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'student':
            return view_func(request, *args,**kwargs)
    return wrapper_function




def registry_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'hod':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('hoddashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'registry':
            return view_func(request, *args,**kwargs)
    return wrapper_function




def bursary_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'hod':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('hoddashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'bursary':
            return view_func(request, *args,**kwargs)
    return wrapper_function



def lecturer_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'hod':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('hoddashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        if group == 'lecturer':
            return view_func(request, *args,**kwargs)
    return wrapper_function





def hod_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'hod':
            return view_func(request, *args,**kwargs)
    return wrapper_function



def supervisor_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'library':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('librarydashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'supervisor':
            return view_func(request, *args,**kwargs)
    return wrapper_function



def library_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group= None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'student':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('studentdashboard')
        elif group == 'registry':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('registrydashboard')
        elif group == 'bursary':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('bursarydashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        elif group == 'supervisor':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('supervisordashboard')
        elif group == 'lecturer':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('lecturerdashboard')
        elif group == 'admin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'superadmin':
            messages.info(request, "You don't have access to view this page, you can contact the admin for help")
            return redirect('dashboard')
        if group == 'library':
            return view_func(request, *args,**kwargs)
    return wrapper_function
            