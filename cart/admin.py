from django.contrib import admin
from journaling.admin import journaling_admin_site
from .models import Cart,CartItems,ShippingInformation,OrderStatus,ReceivedOrder
from django.urls import path


class CartAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id','transaction_id','customer','complete','date']
    list_display_links = None
    list_filter = ['complete', 'date']   


class CartItemsAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id','cart', 'product', 'quantity', 'date']
    list_display_links = None
    list_filter = ['date']


class ShippingInfoAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id','customer', 'cart', 'city_town_area', 'street_lane_other', 'apartment_suite_building', 'mobile_no', 'date']
    list_display_links = None

class OrderStatusAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ['id','transaction_id', 'status', 'result_code']
    list_display_links = None
    list_filter = ['status', 'result_code', 'transaction_id']


class ReceivedOrderAdmin(admin.ModelAdmin):
    model = ReceivedOrder

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('receivedOrders/', ReceivedOrder.show_orders, name=view_name)
        ]


journaling_admin_site.register(Cart, CartAdmin)
journaling_admin_site.register(CartItems, CartItemsAdmin)
journaling_admin_site.register(ShippingInformation, ShippingInfoAdmin)
journaling_admin_site.register(OrderStatus, OrderStatusAdmin)
journaling_admin_site.register(ReceivedOrder, ReceivedOrderAdmin)



