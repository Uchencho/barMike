from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Enquiry, UserLocation

# Register your models here.
class EnquiryAdmin(admin.ModelAdmin):

    list_display = ['user', 
                    'question', 
                    'created', 
                    'updated', 
                    'answered']

class LocationAdmin(OSMGeoAdmin):
    list_display = [
        'name',
        'location',
        'address',
        'city',
    ]

admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(UserLocation, LocationAdmin)