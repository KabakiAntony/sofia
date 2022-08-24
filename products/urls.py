from django.urls import path
from .import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name="list"),
    path('search/', views.search, name="search"),
    path('<slug:slug>/', views.product_details, name="detail"),
]

