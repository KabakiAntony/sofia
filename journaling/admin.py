from django.contrib import admin
from accounts.models import User
from products.models import Product, Category


class JournalingAdmin(admin.AdminSite):
    site_header = 'Journaling Administration'
    site_title = 'Journaling Admin'
    index_title = 'Journaling Admin'

admin_site = JournalingAdmin(name='admin')

admin_site.register(User)
admin_site.register(Category)
admin_site.register(Product)
