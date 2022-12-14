import json
import time
import os
import uuid
from django.contrib import messages
from django.template.loader import render_to_string  
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItems, ShippingInformation, OrderStatus
from products.models import Product
from .utils import cart_data, guest_cart
from .order_email_objects import EmailInfo
from cart.utils import cart_data
from journaling.emails import _send_email
from journaling.kopokopoHandler import KopoKopoHandler


handler = KopoKopoHandler()
email_maker = EmailInfo()


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
        messages.add_message(request, messages.SUCCESS, f"{cartItem} added to cart successfully." )

    elif action == "remove":
        cartItem.quantity = (cartItem.quantity - 1)
        messages.add_message(request, messages.ERROR, f"{cartItem} removed from cart.")

    cartItem.save()

    if cartItem.quantity <= 0 or action == "delete":
        cartItem.delete()
        messages.add_message(request, messages.INFO, f"{cartItem} removed from cart.")

    return JsonResponse("Ok", safe=False)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    cart = data['cart']
    cartItems = data['cartItems']

    if cartItems == 0:
        messages.add_message(request, messages.ERROR, 
        "You don't have any items on cart, please add some & try again.")
        return redirect('cart:cart')
    else:
        context = { "items": items, "cart": cart, "cartItems":cartItems }
        return render(request, "cart/checkout.html", context)


def process_order(request):
    data = cart_data(request)
    items = data['items']
    cart = data['cart']
    cartItems = data['cartItems']
    
    transaction_id = uuid.uuid4()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, cart = guest_cart(request, data)
    
    total = int(data['personal_info']['total'])
    cart.transaction_id = transaction_id

    email_maker.transaction_id = transaction_id # set trx id
    shipping_or_pickup = data['shipping_info']['shipping_or_pickup']
    shipping_or_pickup_info = {
       "city_town_area" : data['shipping_info']['city_town_area'],
        "street_lane_other" : data['shipping_info']['street_lane_other'],
        "apartment_suite_building" : data['shipping_info']['apartment_suite_building'], 
    }
    
    if (total == cart.get_pickup_n_cart_total) or (total == cart.get_shipping_n_cart_total):
        cart.complete = True
    cart.save()

    shipping, created = ShippingInformation.objects.update_or_create(
            customer=customer,
            cart=cart,
            city_town_area = data['shipping_info']['city_town_area'],
            street_lane_other = data['shipping_info']['street_lane_other'],
            apartment_suite_building = data['shipping_info']['apartment_suite_building'],
            mobile_no=data['shipping_info']['mobile_no']
        )

    valid_phone_no = validify_phone_no(data['shipping_info']['mobile_no'])

    # make stk push request to the number on file
    first_name = data['personal_info']['first_name']
    last_name = data['personal_info']['last_name']
    email = data['personal_info']['email']

    # send email to customer and admin with the order attached.
    current_site = get_current_site(request)
    protocol = request.scheme

    callback_url = f"{protocol}://{current_site.domain}/cart/callback/"
    
    response = handler.make_stk_push(first_name, last_name, valid_phone_no, email, total, callback_url)

    email_maker.checkout_req_url = response.headers.get('location')
    
    email_maker.email_subject = """ Thank you for shopping with us."""
    email_maker.email_object = render_to_string("cart/order_email.html",
        {
        'customer':customer,
        'cart':cart,
        'cartItems':cartItems,
        'items':items,
        'current_site':current_site,
        'protocol':protocol,
        'shipping_or_pickup':shipping_or_pickup,
        'shipping_or_pickup_info':shipping_or_pickup_info,
        })   

    email_maker.customer_email = customer.email
    
    email_maker.admin_email_object = render_to_string("cart/admin_order_email.html",
        {
        'customer':customer,
        'shipping':shipping,
        'cart':cart,
        'cartItems':cartItems,
        'items':items,
        'current_site':current_site,
        'protocol':protocol,
        'shipping_or_pickup':shipping_or_pickup,
        'shipping_or_pickup_info':shipping_or_pickup_info,
        })   

    return JsonResponse(response.status_code, safe=False)
    
 
@csrf_exempt
def kopokopo_callback(request):
    """ receive response from kopo kopo  """
    if request.method == 'POST':
        data = json.loads(request.body)
        messages.add_message(request, messages.INFO, 
        "Please hold as we process your payment.")
       
        
    return JsonResponse("Ok", safe=False)


def validify_phone_no(phone_number):
    """ get a phone number and return a phone number in the format required"""
    if phone_number[0] == "0":
        phone_number = "+254" + phone_number[1:]
    return phone_number


def payment_status(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    payment_status_url = email_maker.checkout_req_url
    
    # wait for thirty seconds and check transaction
    time.sleep(20)
    response = handler.query_transaction_status(payment_status_url)

    # payment was processed successfully
    if response['data']['attributes']['status'] == 'Success':
        code = "0"
        status = "Your payment has been processed successfully."
        # only send order email on successful payment.
        try:
            customer_email = email_maker.customer_email
            subject = email_maker.email_subject
            content = email_maker.email_object
            _send_email(request, customer_email, subject, content)

            # create order status object
            OrderStatus.objects.create(
            transaction_id = email_maker.transaction_id,
            status=status,
            result_code = code)

            admin_content = email_maker.admin_email_object
            admin_subject = "We have received and order."
            _send_email(request, "kabaki.antony@gmail.com", admin_subject, admin_content)

        except Exception as e:
            # log this error
            print(str(e))

    elif response['data']['attributes']['status'] == 'Failed':
        code = "1"
        status = "We were unable to receive your payment."


    context = {"cartItems":cartItems, "status":status, "code":code}
    return render(request, "cart/order_status.html",context)




