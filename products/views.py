import json
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator

from .models import Product, Category, Product_Entry
from cart.utils import cart_instance


def home(request):
    """ this will show products on the homepage """
    cart = cart_instance(request)
    products = Product.objects.all().order_by("title")
    categories = Category.objects.all()
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    context = {
        "categories": categories,
        'cart': cart,
        "page_objects": page_objects
    }
    return render(request, "products/index.html", context)


def product_details(request, slug):
    cart = cart_instance(request)
    product = Product.objects.get(slug=slug)
    similar_products = Product.objects.filter(
        category=product.category).exclude(slug__iexact=slug)[:6]
    entries = product.product_entry_set.all()

    context = {
        "product": product,
        "entries": entries,
        "similar_products": similar_products,
        "cart": cart
    }
    return render(request, "products/product_detail.html", context)


def search(request):
    """ show the results of a product that a user has searched for """
    cart = cart_instance(request)
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    product_entries = Product_Entry.objects.annotate(
        search=SearchVector("title", "product", "product__title",
                            "product__category__title"))\
        .filter(search=SearchQuery(q)).order_by('title')

    paginator = Paginator(product_entries, 24)
    page_number = request.GET.get('page')
    page_objects = paginator.get_page(page_number)

    context = {
        "page_objects": page_objects,
        'cart': cart,
    }

    return render(request, "products/search.html", context)


def get_product_entry(request):
    data = {}
    if request.method == 'POST':
        sku = json.load(request)['sku']

        entry = Product_Entry.objects.get(sku=sku)
        product = Product.objects.get(id=entry.product.id)

        context = {
            'entry': entry,
            "product": product,
        }
        data = {'rendered_product': render_to_string(
            'products/entry_detail.html', context)}

    return JsonResponse(data)
