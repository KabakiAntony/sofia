from django.urls import path
from .import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name="list"),
    path('search/', views.search, name="search"),
    path('select/', views.get_product_entry, name="selected_product"),
    path('<slug:slug>/', views.product_details, name="product_detail"),
]

