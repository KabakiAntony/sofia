import json

from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Cart, CartItem
from .utils import cart_instance
from .forms import CheckoutForm
from products.models import Product_Entry


def cart(request):
    cart = cart_instance(request)
    context = {"cart": cart}
    return render(request, 'cart/cart.html', context)


def update_logged_in_user_cart_item(request):
    data = json.loads(request.body)
    entry_sku = data['entry_sku']
    action = data['action']

    customer = request.user.customer
    product_entry = Product_Entry.objects.get(sku=entry_sku)
    cart, created = Cart.objects.get_or_create(customer=customer)
    cartItem, created = CartItem.objects.get_or_create(
        cart=cart, product_entry=product_entry)

    if action == "add" or created:
        cartItem.quantity = (cartItem.quantity + 1)
        messages.add_message(request, messages.SUCCESS,
                             f"{cartItem} added to cart successfully.")

    elif action == "remove":
        cartItem.quantity = (cartItem.quantity - 1)
        messages.add_message(request, messages.ERROR,
                             f"{cartItem} removed from cart.")

    cartItem.save()

    if cartItem.quantity <= 0 or action == "delete":
        cartItem.delete()
        messages.add_message(request, messages.INFO,
                             f"{cartItem} removed from cart.")

    return JsonResponse("Ok", safe=False)


def checkout(request):
    cart = cart_instance(request)
    form = CheckoutForm()

    if cart['total_items_on_cart'] == 0:
        messages.add_message(request, messages.ERROR,
                             "You don't have any items on cart, please add some & try again.")
        return redirect('products:list')
    else:
        context = {
            "cart": cart,
            "form": form,
        }

    return render(request, "cart/checkout.html", context)
