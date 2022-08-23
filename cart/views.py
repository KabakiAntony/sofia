from django.shortcuts import render
# from products.models import Product
# from accounts.models import User, Customer
from .models import Cart, CartItems

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = cart.cartitems_set.all()
    else:
        items = []
        cart = {
            'get_cart_total':0,
            'get_cart_items':0,
        }
    
    context = {
            "items": items,
            "cart": cart,       
            }
    return render(request, 'cart/cart.html', context)




