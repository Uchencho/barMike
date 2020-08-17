from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

class MyUserAdmin(UserAdmin):

    list_display = ['email', 
                    'username', 
                    'first_name', 
                    'phone_number', 
                    'is_active',
                    'is_superuser']

admin.site.register(User, MyUserAdmin)
