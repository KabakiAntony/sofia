from journaling.admin import journaling_admin_site
from django.contrib import admin
from .models import Customer, Address, Region, Area, ShippingCosts


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'get_first_name', 'get_last_name']
    list_display_links = ['user']

    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['customer', 'region', 'area', 'street_lane_other', 'apartment_suite_building', 'mobile_no']
    list_display_links = ['customer']


class RegionAdmin(admin.ModelAdmin):
    list_display = ['region']
    list_display_links = ['region']


class AreaAdmin(admin.ModelAdmin):
    list_display = ['area']
    list_display_links = ['area']

class ShippingCostAdmin(admin.ModelAdmin):
    list_display = ['area', 'cost']
    list_display_links = ['area']



journaling_admin_site.register(Customer, CustomerAdmin)
journaling_admin_site.register(Address, AddressAdmin)
journaling_admin_site.register(Region, RegionAdmin)
journaling_admin_site.register(Area, AreaAdmin)
journaling_admin_site.register(ShippingCosts, ShippingCostAdmin)