from django.contrib import admin

from journaling.admin import journaling_admin_site
from .models import Order, OrderItem, Payment

class OrderAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['customer', 'order_date', 'order_total', 'shipping_cost', 'shipping_or_pickup']
    list_display_links = None
    list_filter = ['customer']   


class OrderItemAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['product_entry', 'quantity']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'transaction_id', 'amount', 'paid_at', 'status']
    list_filter = ['order']


journaling_admin_site.register(Order, OrderAdmin)
journaling_admin_site.register(OrderItem, OrderItemAdmin)
journaling_admin_site.register(Payment, PaymentAdmin)
