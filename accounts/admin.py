from django.contrib import admin
from .models import User


class JournalingAdmin(admin.AdminSite):
    site_header = 'Journaling Administration'
    site_title = 'Journaling Admin'
    index_title = 'Journaling Admin'

admin_site = JournalingAdmin(name='admin')

admin_site.register(User)
