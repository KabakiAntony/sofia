from django.urls import path
from .import views 

app_name = "cart"

urlpatterns = [
    path('', views.cart, name="cart"),
    path('update/', views.update_item, name='update'),
    path('checkout/', views.checkout, name="checkout"),

]
