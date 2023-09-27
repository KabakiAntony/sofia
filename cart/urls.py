from django.urls import path
from .import views 

app_name = "cart"

urlpatterns = [
    path('', views.cart, name="cart"),
    path('update/', views.update_logged_in_user_cart_item, name='update'),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.process_order, name="process_order"),
    path('callback/', views.kopokopo_callback, name="callback"),
    # path('payment-status/', views.payment_status, name="payment_status"),
]
