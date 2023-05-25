from django.contrib import admin
from .models import Vendor




class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')  # display the list display 
    list_display_links = ('user', 'vendor_name')   # show the links 




# Register your models here.
admin.site.register(Vendor , VendorAdmin)