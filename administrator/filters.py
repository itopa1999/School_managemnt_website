import django_filters
from django_filters import DateFilter
from .models import *

class studentsFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields =['department','adm_year','faculty','level','program']
        
        
class studentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields =['matric_no','department','faculty','age']
        

class student1Filter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields =['name','matric_no','department','faculty','level','program']
        

class ResultFilter(django_filters.FilterSet):
    class Meta:
        model = Result
        fields =['student','course','cu','grade','qp']
        

class AccessFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields =['matric_no','department','adm_year']
        
        
class Access1Filter(django_filters.FilterSet):
    class Meta:
        model = Lecturer
        fields =['name' ,'staff_ID']
        
        

class DebitFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields =['schoollevy']
        
        
        
        