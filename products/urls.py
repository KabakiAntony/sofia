from django.urls import path
from .import views

app_name = 'products'

urlpatterns = [
    path('', views.home_page, name="list"),
    path('<slug:slug>/', views.product_details, name="detail"),
]

