from django.contrib import admin
from .models import Enquiry

# Register your models here.
class EnquiryAdmin(admin.ModelAdmin):

    list_display = ['user', 
                    'question', 
                    'created', 
                    'updated', 
                    'answered']

admin.site.register(Enquiry, EnquiryAdmin)