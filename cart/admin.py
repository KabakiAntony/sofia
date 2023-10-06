from django.contrib import admin
from sofia.admin import sofia_admin_site
from .models import Cart, CartItem


class CartAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'customer']
    list_display_links = None
    list_filter = ['customer']


class CartItemAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id', 'cart', 'product_entry', 'quantity', 'created_at']
    list_display_links = None
    list_filter = ['created_at']


sofia_admin_site.register(Cart, CartAdmin)
sofia_admin_site.register(CartItem, CartItemAdmin)
