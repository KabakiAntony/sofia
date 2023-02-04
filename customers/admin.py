from journaling.admin import journaling_admin_site
from django.contrib import admin
from .models import Customer, Address, Region


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_first_name', 'get_last_name', 'mobile_no']
    list_display_links = ['user']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'region', 'street_lane_other', 'apartment_suite_building']
    list_display_links = ['customer']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


journaling_admin_site.register(Customer, CustomerAdmin)
journaling_admin_site.register(Address, AddressAdmin)
journaling_admin_site.register(Region, RegionAdmin)