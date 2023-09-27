from django.urls import path
from .import views

app_name = 'customers'

urlpatterns = [
    path('profile/', views.user_profile, name="profile"),
    path('address/', views.add_address, name="address"),
    path('orders/', views.get_orders, name="orders"),
    path('areas/', views.get_areas, name='areas'),
    path('address/update/', views.update_address, name="update_address"),
    path('get-shipping-cost/', views.get_shipping_cost, name="get-shipping-cost"),
    path('get-pickup-id/', views.get_pickup_id, name="get-pickup-id"),
]
