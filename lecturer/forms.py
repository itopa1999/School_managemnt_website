from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from users.models import *
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from administrator.models import *
from .models import *


class UserForm2(UserCreationForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    user = forms.CharField(max_length=30,initial='Y')
    class Meta:
        model = User
        fields = ['first_name','userid','password1', 'password2','phone','profile_pic','email','dep']
        
        
class StudentResultForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    class Meta:
        model = LecturerResult
        fields = '__all__'
        exclude=['date']
        
        
        
class LecturerForm1(forms.ModelForm):
    date_of_birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    class Meta:
        model=Lecturer
        fields='__all__'
        exclude=['phone_no','email','profile_pic','access',
                 'attaccess','examaccess','department','faculty','user']
        
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'