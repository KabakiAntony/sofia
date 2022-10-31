from django.contrib import admin

class JournalingAdmin(admin.AdminSite):
    site_header = 'Journaling Administration'
    site_title = 'Journaling Admin'
    index_title = 'Journaling Admin'
    site_url = None


journaling_admin_site = JournalingAdmin(name='admin')