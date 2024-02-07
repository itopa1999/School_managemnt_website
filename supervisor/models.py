from django.db import models
from administrator.models import *
# Create your models here.


class Examination(models.Model):
    course=models.ForeignKey(Course, null=True,on_delete=models.CASCADE,blank=True)
    department=models.ForeignKey(Department, null=True,on_delete=models.CASCADE,blank=True)
    faculty=models.ForeignKey(Faculty, null=True,on_delete=models.CASCADE,blank=True)
    total_student=models.IntegerField(blank=True,null=True,default=0)
    present_student=models.IntegerField(blank=True,null=True,default=0)
    absence_student=models.IntegerField(blank=True,null=True,default=0)
    co_supervisor1=models.CharField(max_length=30,blank=True,null=True)
    co_supervisor2=models.CharField(max_length=30,blank=True,null=True)
    co_supervisor3=models.CharField(max_length=30,blank=True,null=True)
    co_supervisor4=models.CharField(max_length=30,blank=True,null=True)
    time_start=models.TimeField(blank=True,null=True)
    time_end=models.TimeField(blank=True,null=True)
    supervisor=models.CharField(max_length=30,blank=True,null=True)
    
    def save(self, *args, **kwargs):  
        self.absence_student = self.total_student - self.present_student 
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course}"
    

class Malpractice(models.Model):
    student=models.ForeignKey(Student, null=True,on_delete=models.CASCADE,blank=True)
    course=models.ForeignKey(Course, null=True,on_delete=models.CASCADE,blank=True)
    action=models.CharField(max_length=250,blank=True,null=True)
    image=models.ImageField(null=True, blank=True)
    supervisor=models.CharField(max_length=30,blank=True,null=True)
    def __str__(self):
        return f"{self.course}"
    
    

