from django.contrib import admin
from accounts.models import User, Customer
from products.models import Product, Category
from cart.models import Cart, CartItems


class JournalingAdmin(admin.AdminSite):
    site_header = 'Journaling Administration'
    site_title = 'Journaling Admin'
    index_title = 'Journaling Admin'

admin_site = JournalingAdmin(name='admin')

admin_site.register(User)
admin_site.register(Customer)
admin_site.register(Category)
admin_site.register(Product)
admin_site.register(Cart)
admin_site.register(CartItems)
