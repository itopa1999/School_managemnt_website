from django import forms
from django.contrib.auth.models import User
from administrator import models as QMODEL
from library import models as MYMODEL
from django.contrib.auth.forms import PasswordChangeForm

class BookForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=QMODEL.Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    class Meta:
        model=MYMODEL.Book
        fields=['name','isbn','author']
        
        
        
class IssuedBookForm(forms.ModelForm):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=MYMODEL.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    studentID=forms.ModelChoiceField(queryset=MYMODEL.Student.objects.all(),empty_label="Choose student", to_field_name="id")
    class Meta:
        model=MYMODEL.IssuedBook
        fields=['expirydate','department']
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'