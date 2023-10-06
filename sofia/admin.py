from django.contrib import admin


class SofiaAdmin(admin.AdminSite):
    site_header = 'Sofia Administration'
    site_title = 'Sofia Admin'
    index_title = 'Sofia Admin'
    site_url = None


sofia_admin_site = SofiaAdmin(name='admin')
