import json
from products.models import Product
from accounts.models import Customer
from .models import Cart, CartItems

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {
        'get_cart_total':0, 
        'get_cart_items':0,
        'get_shipping_amount':350,
        'get_pickup_amount':100,
        'get_shipping_n_cart_total':0,
        'get_pickup_n_cart_total':0,
        }
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'description':product.description,
                        'thumb':product.main_image,
                        'slug':product.slug,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                }
            items.append(item)
        except:
            pass

    order['get_shipping_n_cart_total'] = order['get_cart_total'] + order['get_shipping_amount']
    order['get_pickup_n_cart_total'] = order['get_cart_total'] + order['get_pickup_amount']

    return { "items": items, "cart": order, "cartItems":cartItems }

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)
        items = cart.cartitems_set.all()
        cartItems = cart.get_cart_items

    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        cart = cookie_data['cart']
        cartItems = cookie_data['cartItems']

    return { "items": items, "cart": cart, "cartItems":cartItems }

def guest_cart(request, data):
    email = data['personal_info']['email']
    first_name = data['personal_info']['first_name']
    last_name = data['personal_info']['last_name']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']
    
    name = " ".join([first_name, last_name])
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    cart = Cart.objects.create(
        customer=customer,
        complete=False,
    )
    
    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        CartItems.objects.create(
            product=product,
            cart=cart,
            quantity=item['quantity']
        )

    return customer, cart