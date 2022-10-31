from django.contrib import admin
from journaling.admin import journaling_admin_site
from .models import User, Customer


class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id','first_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'email_confirmed', 'reset_password']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_active', 'email_confirmed']

class CustomerAdmin(admin.ModelAdmin):
    empty_value_display = 'Guest Shopper'
    list_display = ['id','user', 'name', 'email']
    list_display_links = ['email']

journaling_admin_site.register(User, UserAdmin)
journaling_admin_site.register(Customer, CustomerAdmin)
