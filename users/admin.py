from django.contrib import admin
from .models import *
from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    models =  User
    add_form = CustomUserCreationForm
    list_display = ('userid', 'email', 'first_name',)
    fieldsets = (
    (None, {'fields': ('userid', 'password', 'email', 'first_name','last_name', 'groups', 'user_permissions','is_active', 'is_staff', 'is_superuser','date_joined', 'last_login',  )}),
    
    ('Other info',{'fields': ('dep','phone','phone_token','email_token','forgot_password','token','profile_pic','department','nationality',
                'state_of_origin','local_government','account_no','account_bank',
                'qualification','position')}),
    )
    add_fieldsets = (
    (None, {
    'classes': ('wide',),
    'fields': ('userid','password1', 'password2'),
    }),
    )
    ordering = ('userid',)
    search_fields = ('userid',)
    filter_horizontal = ()



admin.site.register(User, CustomUserAdmin)
