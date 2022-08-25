from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q


def home(request):
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

def search(request):
    """ show the results of a product that a user has searched for """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(
        Q(name__contains=q)|
        Q(description__icontains=q)|
        Q(category__name__icontains=q))
    context = {
        "products":products,
    }
    return render(request, "products/search.html", context)


