from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import PasswordChangeForm
from administrator import models as QMODEL
      
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
        
        
class RecordForm(forms.ModelForm):
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=Lecturer.objects.all(),empty_label="Choose Course", to_field_name="id")

    class Meta:
        model=Examination
        fields='__all__'
        exclude=['faculty','department','course']
        
        
        
class MalpracticeForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")

    class Meta:
        model=Malpractice
        fields='__all__'
        exclude=['student','course']
       