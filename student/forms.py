from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from users import models as UMODEL
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from administrator.models import *
from library import models as LMODEL



class UserForm1(UserCreationForm):
    level = [
    ('ND', 'ND'),
    ('HND', 'HND'),
]
    program = [
    ('Full time', 'Full time'),
    ('Part time', 'Part time'),
]
    level= forms.ChoiceField(choices=level)
    program= forms.ChoiceField(choices=program)
    year= forms.IntegerField()
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    class Meta:
        model = UMODEL.User
        fields = ['first_name','userid','password1', 'password2','phone','profile_pic','email','dep']
        
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
        
class LibraryForm(forms.ModelForm):
    class Meta:
        model = LMODEL.Student
        fields = '__all__'
        
        
