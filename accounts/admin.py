from django.contrib import admin
from sofia.admin import sofia_admin_site
from .models import User


class UserAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'first_name', 'email', 'is_staff', 'is_active',
                    'is_superuser', 'last_login', 'date_joined', 'email_confirmed', 'reset_password']
    list_display_links = ['email']
    list_filter = ['is_staff', 'is_active', 'email_confirmed']


sofia_admin_site.register(User, UserAdmin)
