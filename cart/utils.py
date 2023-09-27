import json
from products.models import Product_Entry
from customers.models import Customer
from .models import Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_cart_total':0, 
        'get_cart_items':0,
        }
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            entry = Product_Entry.objects.get(sku=i)
            total = (entry.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                    'product_entry':{
                        'sku':entry.sku,
                        'title':entry.title,
                        'price':entry.price,
                        'description':entry.description,
                        'product':entry.product,
                        'image_set':entry.image_set.all(),
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                }
            items.append(item)
        except:
            pass

    return { "items": items, "cart": order, "cartItems":cartItems }

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, _ = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cartItems = cart.get_cart_items

    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        cart = cookie_data['cart']
        cartItems = cookie_data['cartItems']

    return { "items": items, "cart": cart, "cartItems":cartItems }

def guest_cart(request, data):
    email = data['customer_info']['email']
    firstname = data['customer_info']['first_name']
    lastname = data['customer_info']['last_name']
    is_guest = True

    user, _ = User.objects.get_or_create(
        email=email,
        first_name=firstname,
        last_name=lastname,
        is_guest=is_guest
        )
    
    customer = user.customer

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    cart = Cart.objects.create(
        customer=customer,
    )
    
    for item in items:
        entry = Product_Entry.objects.get(sku=item['product_entry']['sku'])

        CartItem.objects.create(
            product_entry=entry,
            cart=cart,
            quantity=item['quantity']
        )

    return customer, cart