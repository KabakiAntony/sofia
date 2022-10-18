import json
import time
import datetime
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
from journaling.emails import send_email
from journaling.mpesa_handler import MpesaHandler

handler = MpesaHandler()
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
        messages.add_message(request, messages.ERROR, f"1 unit of {cartItem} removed from cart.")

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
    
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = Cart.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, cart = guest_cart(request, data)
    
    total = float(data['personal_info']['total'])
    cart.transaction_id = transaction_id

    email_maker.transaction_id = transaction_id # set trx id
    
    if (total == cart.get_pickup_n_cart_total) or (total == cart.get_shipping_n_cart_total):
        cart.complete = True
    cart.save()

    shipping, created = ShippingInformation.objects.get_or_create(
            customer=customer,
            cart=cart,
            city_town_area = data['shipping_info']['city_town_area'],
            street_lane_other = data['shipping_info']['street_lane_other'],
            apartment_suite_building = data['shipping_info']['apartment_suite_building'],
            mobile_no=data['shipping_info']['mobile_no']
        )

    shipping.save()

    valid_phone_no = validify_phone_no(data['shipping_info']['mobile_no'])

    push_payload = {
        "amount":1,
        "phone_number":valid_phone_no
    }
    # make stk push request to the number on file
    response = handler.make_stk_push(push_payload)
    
    email_maker.checkout_req_id = response.get('CheckoutRequestID')

    response_code = response.get('ResponseCode')
    
    # send email to customer and admin with the order attached.
    current_site = get_current_site(request)
    protocol = request.scheme
    

    email_maker.email_subject = """ Thank you for shopping with us."""
    email_maker.email_object = render_to_string("cart/order_email.html",
        {
        'customer':customer,
        'cart':cart,
        'cartItems':cartItems,
        'items':items,
        'current_site':current_site,
        'protocol':protocol,
        })   

    email_maker.customer_email = customer.email

    return JsonResponse(response_code, safe=False)
    
 
@csrf_exempt
def mpesa_callback(request):
    """ receive response from mpesa  """
    if request.method == 'POST':
        data = json.loads(request.body)
        result_code = data['Body']["stkCallback"]["ResultCode"]
        status = data['Body']["stkCallback"]["ResultDesc"]

        if result_code == 0:
            result_code = 0

        else:
            result_code = 1
        
        OrderStatus.objects.create(
            transaction_id = email_maker.transaction_id,
            status=status,
            result_code = result_code
        )
    return JsonResponse("Ok", safe=False)


def validify_phone_no(phone_number):
    """ get a phone number and return a phone number in the format required"""
    if phone_number[0] == "0":
        phone_number = "254" + phone_number[1:]
    return phone_number


def thank_you(request):
    cartItems = 0
    req_id = email_maker.checkout_req_id
    # wait for one minute and check the status of the transaction
    time.sleep(30) 
    response = handler.query_transaction_status(req_id)

    # payment was processed successfully
    if response['ResultCode'] == '0':
        status = "Your payment has been processed successfully."
        # only send order email on successful payment.
        try:
            customer_email = email_maker.customer_email
            subject = email_maker.email_subject
            content = email_maker.email_object
            send_email(request, customer_email, subject, content)

        except Exception as e:
            print(str(e))

    # user cancelled the push request
    elif response['ResultCode'] == '1032':
        status = "You cancelled our payment request."

    # user did not respond to push request so it timedout
    elif response['ResultCode'] == '1037':
        status = "We were unable to get any response from you for the payment request."

    context = {"cartItems":cartItems, "status":status}
    return render(request, "cart/thank_you.html",context)




