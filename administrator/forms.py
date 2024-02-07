from django import forms
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm,UserChangeForm
from .models import User
from django.forms import ModelForm
from django.forms.widgets import NumberInput
from .models import *
from django.contrib.auth.models import Group




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['level','program','adm_year','faculty','department','phone_no','profile_pic','email','matric_no','name']
        
class StudentForm1(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['level','program','adm_year','faculty','department','phone_no','profile_pic','email',
                   'matric_no','name','user','access','resultaccess','examaccess','adminstatus']

class LecturerForm(UserChangeForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    class Meta:
        model = User
        fields = ['userid','first_name' ,'phone','email','profile_pic','groups']
        
  

class LecturerForm2(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'
        exclude = ['staff_ID','name' ,'phone_no','email','profile_pic','user','faculty','department','access',
                   'attaccess','examaccess']
        
        

class GroupchangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['groups']
       
        
        

class ResultForm(ModelForm):
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    class Meta:
        model = Result
        fields = '__all__'
        exclude=['course','student']


class FacultyForm(ModelForm):
    token=forms.CharField(max_length=10)
    class Meta:
        model = Faculty
        fields = '__all__'
        
class FacultyForm1(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'

        
class CourseForm1(ModelForm):
    token=forms.CharField(max_length=10)
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    lecturerID=forms.ModelChoiceField(queryset=Lecturer.objects.all(),empty_label="Choose Lecturer", to_field_name="id")
    class Meta:
        model = Course
        fields = ['name','course_unit','semester','created_by']

class CourseForm2(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
          
        
        
class MessageForm(ModelForm):
    lecturerID=forms.ModelChoiceField(queryset=Lecturer.objects.all(),empty_label="Choose Lecturer to view message", to_field_name="id",required = False,)
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student to view message", to_field_name="id",required = False,)
    groupID=forms.ModelChoiceField(queryset=Group.objects.all(),empty_label="Choose Group to view message", to_field_name="id",required = False,)
    class Meta:
        model = Message
        fields = '__all__'
        exclude=['group','lecturer','student']
        
        
        
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
class LevyForm(ModelForm):
    class Meta:
        model = Schoollevy
        fields = '__all__'



class DepartmentForm(forms.ModelForm):
    token=forms.CharField(max_length=10)
    facultyID=forms.ModelChoiceField(queryset=Faculty.objects.all(),empty_label="Choose Faculty", to_field_name="id")
    class Meta:
        model = Department
        fields = '__all__'
        exclude=['faculty']
        
        
class DepartmentForm1(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
    

    
class FileForm(ModelForm):
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    class Meta:
        model = File
        fields = '__all__'
        exclude=['student']



class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','userid','password1', 'password2','department','nationality',
                'state_of_origin','local_government','account_no','account_bank','address',
                'qualification','profile_pic','phone','email','dep','position']
        
class UserForm1(UserChangeForm):
    class Meta:
        model = User
        fields = ['first_name','department','nationality','address',
                'state_of_origin','local_government','account_no','account_bank',
                'qualification','profile_pic','phone','email','dep','position']

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = '__all__'
        
class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('userid','groups',)
  
         
class QuestionForm(forms.ModelForm):
    
    #this will show dropdown __str__ method course model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in course model and return it
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model=Question
        fields=['marks','question','option1','option2','option3','option4','answer','user']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }
        
class NoticeForm(forms.ModelForm):
    class Meta:
        model=Notice
        fields='__all__'
        
        
class PayrollForm(forms.ModelForm):
    class Meta:
        model=Staff_Payroll
        fields='__all__'
        exclude=['r_sal']
     
     
class StatusForm(forms.ModelForm):
    class Meta:
        model=Status
        fields='__all__'
        exclude=['expiry']
        
        
class TableForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model=Timetable
        fields='__all__'
        exclude=['department','course']
        


class ExamTableForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model=Exam_Timetable
        fields='__all__'
        exclude=['department','course']
        

        
class DepartmentNoticeForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department to view this notice", to_field_name="id")
    class Meta:
        model=DepartmentNotice
        fields='__all__'
        exclude=['department']
    
    
    
class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields='__all__'
        
        
   
        
        
class DebitForm(forms.ModelForm):
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    schoollevyID=forms.ModelChoiceField(queryset=Schoollevy.objects.all(),empty_label="Choose Levy", to_field_name="id")
    class Meta:
        model=Transaction
        fields='__all__'
        exclude=['date','remain','credit','student','schoollevy']
        
        
class CreditForm(forms.ModelForm):
    studentID=forms.ModelChoiceField(queryset=Student.objects.all(),empty_label="Choose Student", to_field_name="id")
    schoollevyID=forms.ModelChoiceField(queryset=Schoollevy.objects.all(),empty_label="Choose Levy", to_field_name="id")
    class Meta:
        model=Transaction
        fields='__all__'
        exclude=['date','remain','debit','schoollevy','student']
        
        
class AttendanceForm(forms.ModelForm):
    departmentID=forms.ModelChoiceField(queryset=Department.objects.all(),empty_label="Choose Department", to_field_name="id")
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model=Attendance
        fields='__all__'
        exclude=['absence_student','credit','course','department']
        
        


class RegistercourseForm(forms.ModelForm):
    courseID=forms.ModelChoiceField(queryset=Course.objects.all(),empty_label="Choose Course", to_field_name="id")
    class Meta:
        model=Register_course
        fields='__all__'
        exclude=['course']