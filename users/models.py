from django.db import models
from django.contrib.auth.models import AbstractUser
from.manager import UserManager
from student.utils import generate_code
# Create your models here.



class User(AbstractUser):
    username = None
    userid=models.CharField(max_length=15, unique=True)
    phone=models.IntegerField(null=True,blank=True)
    dep=models.CharField(max_length=20,null=True,blank=True)
    phone_token=models.CharField(max_length=15,blank=True)
    email_token=models.CharField(max_length=50,blank=True)
    forgot_password=models.CharField(max_length=20,blank=True)
    token=models.CharField(max_length=20,blank=True)
    department = models.CharField(max_length=200, blank=True,null=True)
    nationality = models.CharField(max_length=200, blank=True,null=True)
    state_of_origin = models.CharField(max_length=200, blank=True,null=True)
    local_government = models.CharField(max_length=200,blank=True, null=True)
    address = models.CharField(max_length=200,blank=True, null=True)
    account_no = models.IntegerField(blank=True,null=True)
    account_bank = models.CharField(max_length=200, blank=True,null=True)
    qualification = models.CharField(max_length=200, blank=True,null=True)
    position = models.CharField(max_length=200, blank=True,null=True)
    profile_pic=models.ImageField(default='profilepic.png',null=True,blank=True)
    
    def save(self, *args, **kwargs):
        if self.token == "":
            self.token = generate_code()
        return super().save(*args, **kwargs)
    

    
    objects=UserManager( )
    
    USERNAME_FIELD ='userid'
    REQUIRED_FIELDS=[]
    