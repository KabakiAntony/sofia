from django.urls import path
from .import views

app_name = "cart"

urlpatterns = [
    path('cart/', views.cart, name="cart"),
    path('update/', views.update_logged_in_user_cart_item, name='update'),
    path('checkout/', views.checkout, name="checkout"),
]
