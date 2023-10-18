import json
from products.models import Product_Entry
from customers.models import Customer
from .models import Cart, CartItem

from django.contrib.auth import get_user_model

User = get_user_model()


def cookie_cart_instance(request):
    """
    Construct a guest cart based of items
    they have selected.
    """
    try:
        cookie_cart_entry = json.loads(request.COOKIES['cart'])
    except:
        cookie_cart_entry = {}

    items = []
    cart_total = 0
    total_items_on_cart = 0

    for sku in cookie_cart_entry:
        try:
            entry = Product_Entry.objects.get(sku=sku)
            total = (entry.price * cookie_cart_entry[sku]['quantity'])

            cart_total += total
            total_items_on_cart += cookie_cart_entry[sku]['quantity']

            item = {
                'product_entry': {
                    'sku': entry.sku,
                    'title': entry.title,
                    'price': entry.price,
                    'description': entry.description,
                    'product': entry.product,
                    'image_set': entry.image_set.all(),
                },
                'quantity': cookie_cart_entry[sku]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass

    return {
        "items": items,
        "cart_total": cart_total,
        "total_items_on_cart": total_items_on_cart
    }


def cart_instance(request):
    """
    return a cart whether one is guest or authenticated
    """
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, _ = Cart.objects.get_or_create(customer=customer)
        items = cart.cartitem_set.all()
        cart_total = cart.cart_total
        total_items_on_cart = cart.total_items_on_cart

    else:
        cookie_cart = cookie_cart_instance(request)
        items = cookie_cart['items']
        cart_total = cookie_cart["cart_total"]
        total_items_on_cart = cookie_cart["total_items_on_cart"]

    cart = {
        "items": items,
        "cart_total": cart_total,
        "total_items_on_cart": total_items_on_cart
    }

    return cart


def persist_guest_cart(request, data):
    """
    persist guest cart into the db
    """
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

    cookie_data = cookie_cart_instance(request)
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
