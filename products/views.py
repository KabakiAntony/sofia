from django.shortcuts import render
from .models import Product, Category


def home_page(request):
    """ this will show products on the homepage """
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "categories":categories,
        "products":products,
    }
    return render(request, "products/index.html", context)


def product_details(request, slug):
    """ Show the details of an individual product"""
    product = Product.objects.get(slug=slug)
    context = {
        "product":product
    }
    return render(request, "products/product_detail.html", context)


