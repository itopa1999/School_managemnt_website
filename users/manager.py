from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations =True
    
    
    def create_user(self, userid,password=None, **extra_fields):
        
        if not userid:
            raise ValueError('Userid is required')
        
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, userid, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('super user must have is_staff true'))
        
        return self.create_user(userid, password,**extra_fields)