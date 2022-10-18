from django.urls import path
from .import views 

app_name = "cart"

urlpatterns = [
    path('', views.cart, name="cart"),
    path('update/', views.update_item, name='update'),
    path('checkout/', views.checkout, name="checkout"),
    path('process_order/', views.process_order, name="process_order"),
    path('callback/', views.mpesa_callback, name="callback"),
    path('thank-you/', views.thank_you, name="thank_you"),
]
