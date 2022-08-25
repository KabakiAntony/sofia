from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import Cart, CartItems
from products.models import Product
from accounts.models import User, Customer

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = cart.cartitems_set.all()

    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0, }
    
    context = { "items": items, "cart": cart,}
    return render(request, 'cart/cart.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['product_id']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
    cartItem, created = CartItems.objects.get_or_create(cart=cart, product=product)     

    if action == "add" or created:
        cartItem.quantity = (cartItem.quantity + 1)
        messages.success(request, f"{cartItem} added to cart successfully.")

    elif action == "remove":
        cartItem.quantity = (cartItem.quantity - 1)
        messages.success(request, f"1 unit of {cartItem} removed from cart.")

    cartItem.save()

    if cartItem.quantity <= 0 or action == "delete":
        cartItem.delete()
        messages.success(request, f"{cartItem} removed from cart.")

    return JsonResponse("Item was added", safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = cart.cartitems_set.all()

    else:
        items = []
        cart = {'get_cart_total':0, 'get_cart_items':0, }
    
    context = { "items": items, "cart": cart,  "customer": customer,}
    return render(request, "cart/checkout.html", context)




