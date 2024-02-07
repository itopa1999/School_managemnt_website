from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone
from django.db.models import Sum
from users.models import *
from lecturer.models import *
from student.models import *
from datetime import datetime,timedelta

# Create your models here.

class Faculty(models.Model):
    name = models.CharField(max_length=200, null=True)
    name_of_Hof = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=200, blank=True,null=True)
    created_by= models.CharField(max_length=200, blank=True,null=True)
    date= models.DateField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    hod = models.CharField(max_length=200,null=True)
    description = models.CharField(max_length=200, blank=True,null=True)
    created_by= models.CharField(max_length=200, blank=True,null=True)
    date= models.DateField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
            
            
    def __str__(self):
        return self.name



class Student(models.Model):
    MARITAL_STATUS =(
        ('Married', 'Married'),
        ('Single', 'Single'),
    )
    PROGRAM =(
        ('Full time', 'Full time'),
        ('Part time', 'Part time'),
    )
    COMPLEXION =(
        ('Dark', 'Dark'),
        ('Light', 'Light'),
    )
    LEVEL =(
        ('ND', 'ND'),
        ('HND', 'HND'),
    )
    GRADE=(
        ('A1', 'A1'),('B2', 'B2'),('B3', 'B3'),('C4', 'C4'),('C5', 'C5'),
        ('C6', 'C6'),('D7', 'D7'),('E8', 'E8'),('F9', 'F9'),   
    ) 
    NAME_OF_EXAM=(
        ('WAEC', 'WAEC'),
        ('NECO', 'NECO'),
        ('NABTEB', 'NABTEB'),
    )
    SUBJECT =(
        ('English', 'English'),('Chemitry','Chemitry'), ('Biology','Biology'), ('Lit in English', 'Lit in English'),
        ('Commerce', 'Commerce'), ('Government', 'Government'), ('Agriculture Science', 'Agriculture Science'),
        ('History', 'History'), ('Fine Arts', 'Fine Arts'), ('French', 'French'), ('Further Mathematics', 'Further Mathematics'),
        ('Mathematics', 'Mathematics'), ('Physics', 'Physics'), ('Geography', 'Geography'), ('Economic', 'Economic'),
        ('Account', 'Account'), ('Christian Religious Studies', 'Christian Religious Studies'),
        ('islamic Religious Studies','islamic Religious Studies'), ('music', 'music'), ('Animal Husbandry', 'Animal Husbandry'),
        ('Civic Education', 'Civic Education'), ('Yoruba', 'Yoruba'), ('Home Economic', 'Home Economic'), ('Igbo', 'Igbo'),
        ('Hausa', 'Hausa'), ('Arabic', 'Arabic'),
    )
    
    #.........Student Profile and Informations.
    user= models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    matric_no = models.CharField(max_length=200,null=True)
    jamb_reg=models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200,  blank=True,null=True)
    SEX =(
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=200, blank=True, null=True, choices=SEX)
    access=models.BooleanField(default=True, blank=True)
    resultaccess=models.BooleanField(default=True, blank=True)
    examaccess=models.BooleanField(default=True, blank=True)
    adminstatus=models.BooleanField(default=False, blank=True)
    date_of_birth = models.DateField(max_length=200, blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    place_of_birth = models.CharField(max_length=200, blank=True,null=True)
    marital_status = models.CharField(max_length=200, blank=True,null=True, choices=MARITAL_STATUS)
    postal_address = models.CharField(max_length=200,null=True)
    nationality = models.CharField(max_length=200, blank=True,null=True)
    state_of_origin = models.CharField(max_length=200, blank=True,null=True)
    local_government = models.CharField(max_length=200,blank=True, null=True)
    name_of_parent = models.CharField(max_length=200, blank=True,null=True)
    address_of_parent = models.CharField(max_length=200, blank=True,null=True)
    parent_phone = models.IntegerField(blank=True,null=True)
    program = models.CharField(max_length=200, null=True,choices=PROGRAM)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    level = models.CharField(max_length=200,null=True, choices=LEVEL)
    adm_year=models.IntegerField(null=True)
    complexion = models.CharField(max_length=200, null=True, blank=True,choices=COMPLEXION)
    comment_on_character = models.CharField(max_length=200, blank=True,null=True)
    account_no = models.IntegerField(blank=True,null=True)
    account_bank = models.CharField(max_length=200, blank=True,null=True)
    blood_group = models.CharField(max_length=200, blank=True,null=True)
    crime = models.CharField(max_length=200, blank=True,null=True,)
    profile_pic=models.ImageField(default='profilepic.png',null=True,blank=True)
    #......Student Results Here.........
    
    #.........Student Institution and year +Qualifications
    year = models.CharField(max_length=200, blank=True,null=True)
    exam_no = models.CharField(max_length=200, blank=True,null=True)
    slip_no = models.CharField(max_length=200, blank=True,null=True)
    center_no = models.CharField(max_length=200, blank=True,null=True)
    score= models.IntegerField(blank=True,null=True)
    
    name_exam= models.CharField(max_length=200, blank=True,null=True, choices=NAME_OF_EXAM)
    exam_no1= models.CharField(max_length=200, blank=True,null=True)
    center_no1=models.CharField(max_length=200, blank=True,null=True)
    year_exam=models.CharField(max_length=200, blank=True,null=True)
    sub1 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub2 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub3 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub4 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub5 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub6 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub7 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub8 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub9 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    sub10 = models.CharField(max_length=200, null=True, blank=True,choices=SUBJECT)
    
    gra1 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra2 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra3 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra4 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra5 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra6 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra7 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra8 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra9 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    gra10 = models.CharField(max_length=200, null=True, blank=True,choices=GRADE)
    
    ins1= models.CharField(max_length=200, blank=True,null=True)
    ins2= models.CharField(max_length=200, blank=True,null=True)
    ins3= models.CharField(max_length=200, blank=True,null=True)
    
    sta_ins1= models.IntegerField(blank=True,null=True)
    sta_ins2= models.IntegerField(blank=True,null=True)
    sta_ins3= models.IntegerField(blank=True,null=True)
    
    end_ins1= models.IntegerField(blank=True,null=True)
    end_ins2= models.IntegerField(blank=True,null=True)
    end_ins3= models.IntegerField(blank=True,null=True)
    
    qua_ins1= models.CharField(max_length=200,blank=True,null=True)
    Qua_ins2= models.CharField(max_length=200,blank=True,null=True)
    Qua_ins3= models.CharField(max_length=200,blank=True,null=True)
    gpa=models.FloatField(blank=True, null=True)
    created_by= models.CharField(max_length=200, blank=True,null=True)
    date= models.DateField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
        

 
    

class File(models.Model):
    student= models.ForeignKey(Student,blank=True,null=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=200, blank=True,null=True)
    file= models.FileField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.student}"

class Schoollevy(models.Model):
    name=models.CharField(max_length=200, blank=True,null=True)
    student= models.ForeignKey(Student,blank=True,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class Transaction(models.Model):
    student= models.CharField(max_length=200, blank=True,null=True) 
    department=models.ForeignKey(Department,blank=True,null=True, on_delete=models.CASCADE)
    schoollevy= models.ForeignKey(Schoollevy,blank=True,null=True, on_delete=models.CASCADE)
    credit=models.IntegerField(blank=True,null=True,default=0)
    debit=models.IntegerField(blank=True,null=True,default=0)
    remain=models.IntegerField(blank=True,null=True,default=0)
    descrip=models.CharField(max_length=200, blank=True,null=True) 
    date=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, blank=True,null=True, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student}"


class Lecturer(models.Model):
    SEX =(
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    MARITAL_STATUS =(
        ('Married', 'Married'),
        ('Single', 'Single'),
    )
    COMPLEXION =(
        ('Dark', 'Dark'),
        ('Light', 'Light'),
    )
    user= models.OneToOneField(User, null=True, blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True,)
    staff_ID = models.CharField(max_length=200,null=True,blank=True,)
    access=models.BooleanField(default=True, blank=True)
    attaccess=models.BooleanField(default=True, blank=True)
    examaccess=models.BooleanField(default=True, blank=True)
    faculty = models.ForeignKey(Faculty, null=True,blank=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True,blank=True, on_delete=models.CASCADE)
    phone_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=200,  blank=True,null=True)
    sex = models.CharField(max_length=200, blank=True, null=True, choices=SEX)
    address= models.CharField(max_length=200,null=True)
    date_of_birth = models.DateField(max_length=200, blank=True,null=True)
    age = models.IntegerField(blank=True,null=True)
    place_of_birth = models.CharField(max_length=200, blank=True,null=True)
    marital_status = models.CharField(max_length=200, blank=True,null=True, choices=MARITAL_STATUS)
    nationality = models.CharField(max_length=200, blank=True,null=True)
    state_of_origin = models.CharField(max_length=200, blank=True,null=True)
    local_government = models.CharField(max_length=200,blank=True, null=True)
    hobby = models.CharField(max_length=200, blank=True,null=True)
    complexion = models.CharField(max_length=200, null=True, blank=True,choices=COMPLEXION)
    account_no = models.IntegerField(blank=True,null=True)
    account_bank = models.CharField(max_length=200, blank=True,null=True)
    qualification = models.CharField(max_length=200, blank=True,null=True)
    profile_pic=models.ImageField(default='profilepic.png',null=True,blank=True)
    created_by= models.CharField(max_length=200, blank=True,null=True)
    date= models.DateField(null=True, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
            
            
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.name
    
class Work_Experience1(models.Model):
    lecturer= models.ForeignKey(Lecturer,blank=True,null=True, on_delete=models.CASCADE)
    place = models.CharField(max_length=200, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    achievement = models.CharField(max_length=200, blank=True,null=True)
    
    def __str__(self):
        return f"{self.lecturer}"
    

class Institution_Attended1(models.Model):
    lecturer= models.ForeignKey(Lecturer,blank=True,null=True, on_delete=models.CASCADE)
    place = models.CharField(max_length=200, null=True)
    start = models.IntegerField(blank=True, null=True)
    end = models.IntegerField(blank=True, null=True)
    qua = models.CharField(max_length=200, blank=True,null=True)
    
    def __str__(self):
        return f"{self.lecturer}"

  
class File2(models.Model):
    lecturer= models.ForeignKey(Lecturer,blank=True,null=True, on_delete=models.CASCADE)
    title=models.CharField(max_length=200, blank=True,null=True)
    file= models.FileField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.lecturer}"
    
 


class Course(models.Model):
    SEMESTER =(
        ('ND1 first Semester', 'ND1 first Semester'),('ND1 second Semester', 'ND1 second Semester'),
        ('ND2 first Semester', 'ND2 first Semester'),('ND2 second Semester', 'ND2 second Semester'),
        ('HND1 first Semester', 'HND1 first Semester'),('HND1 second Semester', 'HND1 second Semester'),
        ('HND2 first Semester', 'HND2 first Semester'),('HND2 second Semester', 'HND2 second Semester')
    )
    name=models.CharField(max_length=200, blank=True,null=True)
    course_unit=models.PositiveIntegerField(null=False,default=False)
    faculty = models.ForeignKey(Faculty, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    lecturer= models.ForeignKey(Lecturer,blank=True,null=True, on_delete=models.CASCADE)
    semester=models.CharField(max_length=200, blank=True,null=True, choices=SEMESTER,default='ND1 first Semester')
    created_by= models.CharField(max_length=200, blank=True,null=True)
    date= models.DateField(null=True, blank=True)
    price=models.IntegerField(blank=True,null=True,default=0)
    
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
       
        self.price=self.course_unit * 7000
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.name 
    
        
class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat,default='Option1')
    user=models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.question 

class Result1(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    
    def __str__(self):
        return f"{self.student}"
    
class Result(models.Model):
    student= models.ForeignKey(Student,blank=True,null=True, on_delete=models.CASCADE) 
    course= models.ForeignKey(Course,blank=True,null=True, on_delete=models.CASCADE)
    cu=models.IntegerField(blank=True,null=True)
    exam_score=models.IntegerField(blank=True,null=True)
    test_score=models.IntegerField(blank=True,null=True)
    attendant_score=models.IntegerField(blank=True,null=True)
    grade= models.CharField(max_length=200, blank=True,null=True)  
    qp=models.CharField(max_length=3,blank=True,null=True)
    def save(self):
        total_score=(self.exam_score + self.test_score + self.attendant_score)
        if total_score >=75:
            self.qp =self.cu *4.00
            self.grade =("A")
        elif total_score <=74 and total_score >=70 :
            self.qp =self.cu *3.5
            self.grade =("AB")
        elif total_score <=69 and total_score >=65 :
            self.qp =self.cu *3.25
            self.grade =("B")
        elif total_score <=64 and total_score >=60 :
            self.qp =self.cu *3.00
            self.grade =("BC")
        elif total_score <=59 and total_score >=55 :
            self.qp =self.cu *2.75
            self.grade =("C")
        elif total_score <=54 and total_score >=50 :
            self.qp =self.cu *2.50
            self.grade =("CD")
        elif total_score <=49 and total_score >=45 :
            self.qp =self.cu *2.25
            self.grade =("D")
        elif total_score <=44 and total_score >=40 :
            self.qp =self.cu *2.00
            self.grade =("E")
        else:
            self.qp =self.cu *0
            self.grade =("F")
        return super(Result, self).save()
    
    def __str__(self):
        return f"{self.student}"
    
    
    
class LecturerResult(models.Model):
    student= models.ForeignKey(Student,blank=True,null=True, on_delete=models.CASCADE) 
    course= models.ForeignKey(Course,blank=True,null=True, on_delete=models.CASCADE)
    cu=models.IntegerField(blank=True,null=True)
    exam_score=models.IntegerField(blank=True,null=True)
    test_score=models.IntegerField(blank=True,null=True)
    attendant_score=models.IntegerField(blank=True,null=True)
    grade= models.CharField(max_length=200, blank=True,null=True)  
    qp=models.CharField(max_length=3,blank=True,null=True)
    lecturer=models.ForeignKey(Lecturer,blank=True,null=True, on_delete=models.CASCADE)
    date=models.DateField()
    
    def save(self):
        if self.date is None:
            self.date = timezone.now()
            
        total_score=(self.exam_score  + self.test_score + self.attendant_score)
        if total_score >=75:
            self.qp =self.cu *4.00
            self.grade =("A")
        elif total_score <=74 and total_score >=70 :
            self.qp =self.cu *3.5
            self.grade =("AB")
        elif total_score <=69 and total_score >=65 :
            self.qp =self.cu *3.25
            self.grade =("B")
        elif total_score <=64 and total_score >=60 :
            self.qp =self.cu *3.00
            self.grade =("BC")
        elif total_score <=59 and total_score >=55 :
            self.qp =self.cu *2.75
            self.grade =("C")
        elif total_score <=54 and total_score >=50 :
            self.qp =self.cu *2.50
            self.grade =("CD")
        elif total_score <=49 and total_score >=45 :
            self.qp =self.cu *2.25
            self.grade =("D")
        elif total_score <=44 and total_score >=40 :
            self.qp =self.cu *2.00
            self.grade =("E")
        else:
            self.qp =self.cu *0
            self.grade =("F")
        return super(LecturerResult, self).save()
    
    def __str__(self):
        return f"{self.student}"


class Exam_Timetable(models.Model):
    course=models.ForeignKey(Course, null=True,on_delete=models.CASCADE)
    department=models.ForeignKey(Department, null=True,on_delete=models.CASCADE)
    cat=(('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'))
    week=models.CharField(max_length=200,null=True,choices=cat,default='Monday')
    timefrom=models.TimeField(null=True)
    timeto=models.TimeField(null=True)
    supervisor=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.week
    

class Timetable(models.Model):
    course=models.ForeignKey(Course, null=True,on_delete=models.CASCADE)
    department=models.ForeignKey(Department, null=True,on_delete=models.CASCADE)
    cat=(('Monday','Monday'),('Tuesday','Tuesday'),('Wednesday','Wednesday'),('Thursday','Thursday'),('Friday','Friday'))
    week=models.CharField(max_length=200,choices=cat,default='Monday')
    lecturer=models.ForeignKey(Lecturer, blank=True,null=True,on_delete=models.CASCADE)
    timefrom=models.TimeField(null=True)
    timeto=models.TimeField(null=True)
  
    
    def __str__(self):
        return self.week    
    

    
class Event(models.Model):
     title = models.CharField(max_length=200)
     start_time = models.DateField()
     end_time = models.DateField()
     
     def __str__(self):
        return self.title
     
class Notice(models.Model):
     title = models.CharField(max_length=200)
     description = models.TextField()
     sender= models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
     year=models.IntegerField(null=True)
     profile_pic=models.ImageField(null=True,blank=True)
     date = models.DateField(blank=True)
     
     def __str__(self):
        return self.title
     
     def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    
class DepartmentNotice(models.Model):
     title = models.CharField(max_length=200)
     description = models.TextField()
     department= models.ForeignKey(Department,blank=True,null=True, on_delete=models.CASCADE)
     sender= models.ForeignKey(User,blank=True,null=True, on_delete=models.CASCADE)
     profile_pic=models.ImageField(null=True,blank=True)
     LEVEL =(('ND', 'ND'),('HND', 'HND'))
     level= models.CharField(max_length=200, blank=True,null=True, choices=LEVEL,default="ND")
     year=models.IntegerField(null=True)
     date = models.DateField(blank=True)
     
     def __str__(self):
        return self.title
     
     def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)


class Message(models.Model):
    sender=models.CharField(max_length=50, blank=True,null=True)
    group=models.ForeignKey(Group, null=True, blank=True,default="",on_delete=models.CASCADE)
    student=models.ForeignKey(Student, null=True,blank=True,default="", on_delete=models.CASCADE)
    lecturer=models.ForeignKey(Lecturer, null=True, blank=True,default="",on_delete=models.CASCADE)
    subject=models.CharField(max_length=50, blank=True)
    message=models.TextField(max_length=3000, blank=True)
    profile_pic=models.ImageField(null=True,blank=True)
    date=models.DateTimeField(blank=True)
    
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.subject


    
    
class Attendance(models.Model):
    lecturer= models.CharField(max_length=50, blank=True)
    course=models.ForeignKey(Course, null=True,on_delete=models.CASCADE,blank=True)
    department=models.ForeignKey(Department, null=True,on_delete=models.CASCADE,blank=True)
    total_student=models.IntegerField(blank=True,null=True,default=0)
    present_student=models.IntegerField(blank=True,null=True,default=0)
    absence_student=models.IntegerField(blank=True,null=True,default=0)
    date = models.DateField(blank=True,null=True,)
     
    def __str__(self):
        return str(self.date)
     
    def save(self, *args, **kwargs):
        if self.date is None:
            self.date = timezone.now()
        return super().save(*args, **kwargs)
            
        self.absence_student = self.total_student - self.present_student
        return super().save(*args, **kwargs)
    



class Status(models.Model):
    user=models.CharField(max_length=50, null=True, blank=True)
    status=models.TextField(max_length=240, null=True, blank=True)
    profile_pic=models.ImageField(null=True,blank=True)
    expiry=models.DateTimeField(blank=True,null=True,)
    
    def __str__(self):
        return str(self.status)
    
    def save(self, *args, **kwargs):
        if self.expiry is None:
            self.expiry = timezone.now()
        return super().save(*args, **kwargs)


class Staff_Payroll(models.Model):
    staff=models.CharField(max_length=50, null=True, blank=True)
    salary=models.IntegerField(blank=True,null=True)
    vat=models.IntegerField(blank=True,null=True)
    pension=models.IntegerField(blank=True,null=True)
    r_sal=models.IntegerField(blank=True,null=True)
    
    def save(self, *args, **kwargs):            
        self.r_sal = self.salary - self.vat - self.pension
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.staff
    
    
class Register_course(models.Model):
    SEMESTER =(
        ('ND1 first Semester', 'ND1 first Semester'),('ND1 second Semester', 'ND1 second Semester'),
        ('ND2 first Semester', 'ND2 first Semester'),('ND2 second Semester', 'ND2 second Semester'),
        ('HND1 first Semester', 'HND1 first Semester'),('HND1 second Semester', 'HND1 second Semester'),
        ('HND2 first Semester', 'HND2 first Semester'),('HND2 second Semester', 'HND2 second Semester')
    )
    student=models.ForeignKey(Student, null=True,blank=True, on_delete=models.CASCADE)
    course_unit=models.IntegerField(null=False,blank=True,)
    course=models.ForeignKey(Course, null=True,blank=True, on_delete=models.CASCADE)
    semester=models.CharField(max_length=200, blank=True,null=True, choices=SEMESTER)
   
   
    def __str__(self):
        return str(self.student)