import json
import datetime
from unicodedata import decimal
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Cart, CartItems, ShippingInformation
from products.models import Product
from accounts.models import Customer
from .utils import cookie_cart, cart_data, guest_cart


def cart(request):
    data = cart_data(request)
    items = data['items']
    cart = data['cart']
    cartItems = data['cartItems']

    context = { "items": items, "cart": cart, "cartItems":cartItems }
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

    return JsonResponse("Ok", safe=False)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    cart = data['cart']
    cartItems = data['cartItems']

    if cartItems == 0:
        messages.error(request, "You don't have any items on cart, please add some & try again.")
        return redirect('cart:cart')
    else:
        context = { "items": items, "cart": cart, "cartItems":cartItems }
        return render(request, "cart/checkout.html", context)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, cart = guest_cart(request, data)
    
    total = float(data['personal_info']['total'])
    cart.transaction_id = transaction_id

    if total == cart.get_cart_total:
        cart.complete = True
    cart.save()

    ShippingInformation.objects.create(
            customer=customer,
            cart=cart,
            city_town_area = data['shipping_info']['city_town_area'],
            street_lane_other = data['shipping_info']['street_lane_other'],
            apartment_suite_building = data['shipping_info']['apartment_suite_building'],
            mobile_no=data['shipping_info']['mobile_no']
        )
        
    # send notificatior to mpesa to request for payment
    # send email to customer, email the admin wil the order attached
    
   
    return JsonResponse("Order received", safe=False)



