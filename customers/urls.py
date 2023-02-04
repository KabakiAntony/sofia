from django.urls import path
from .import views

app_name = 'customers'

urlpatterns = [
    path('profile/', views.user_profile, name="profile"),
    path('information/', views.get_user_infomation, name="information"),
    path('address/', views.add_address, name="address"),
    path('orders/', views.get_orders, name="orders"),
]
