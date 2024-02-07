from django.db import models
from administrator.models import Department
from django.contrib.auth.models import User
from datetime import datetime,timedelta
# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=30,blank=True,null=True)
    matric_no=models.CharField(max_length=30,blank=True,null=True)
    department=models.CharField(max_length=30,blank=True,null=True)
    faculty=models.CharField(max_length=30,blank=True,null=True)
    level=models.CharField(max_length=30,blank=True,null=True)
    program=models.CharField(max_length=30,blank=True,null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    name=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    department=models.ForeignKey(Department, null=True,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    student=models.ForeignKey(Student, null=True,on_delete=models.CASCADE,blank=True)
    department=models.CharField(max_length=40,null=True,blank=True)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    def __str__(self):
        return f"{self.department}"
