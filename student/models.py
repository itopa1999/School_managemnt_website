from django.db import models
from users.models import *
from lecturer.models import *
from administrator.models import *
from django.utils import timezone
# Create your models here.
 
class Token(models.Model):
    token_id=models.CharField(max_length=12, blank=True)
    
    
    def save(self, *args, **kwargs):
        if self.token_id == "":
            self.token_id = generate_code()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.student}"
    



# Create your models here.
