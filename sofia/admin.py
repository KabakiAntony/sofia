from django.contrib import admin


class SofiaAdmin(admin.AdminSite):
    site_header = 'Journaling Administration'
    site_title = 'Journaling Admin'
    index_title = 'Journaling Admin'
    site_url = None


sofia_admin_site = SofiaAdmin(name='admin')
