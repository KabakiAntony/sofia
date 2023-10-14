import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.template.loader import render_to_string

from .models import Address, Region, Customer, Area, ShippingCosts
from .forms import AddressForm
from products.models import Product
from cart.utils import cart_data


@login_required(login_url='/accounts/signin/')
def user_profile(request):
    user = request.user
    data = cart_data(request)
    cartItems = data['cartItems']

    try:
        address = Address.objects.get(customer=user.id)

        context = {
            "customer": user.customer,
            "address": address,
            "cartItems": cartItems,
        }

    except ObjectDoesNotExist:
        form = AddressForm()
        context = {
            "customer": user.customer,
            "form": form,
            "cartItems": cartItems,
        }

    return render(request, 'customers/profile.html', context)


@login_required(login_url='/accounts/signin/')
def add_address(request):
    data = cart_data(request)
    cartItems = data['cartItems']

    if request.method == "POST":
        user = request.user
        form = AddressForm(request.POST)

        if form.is_valid():
            customer = Customer.objects.get(id=user.id)

            selected_region = form.cleaned_data.get('region')
            region = Region.objects.get(id=selected_region.id)

            selected_area = form.cleaned_data.get('area')
            area = Area.objects.get(id=selected_area.id)

            mobile_no = form.cleaned_data.get('mobile_no')
            street = form.cleaned_data.get('street_lane_other')
            apartment = form.cleaned_data.get('apartment_suite_building')

            address = Address(
                area=area,
                region=region,
                street_lane_other=street,
                apartment_suite_building=apartment,
                customer=customer,
                mobile_no=mobile_no,
                is_default=True)
            address.save()

            return redirect('customers:profile')

        else:
            for key in form.errors:
                messages.add_message(
                    request, messages.ERROR, str(form.errors[key]))

            context = {
                'form': form,
                "cartItems": cartItems, }

            return render(request, 'customers/profile.html', context)


def get_areas(request):

    if request.method == "POST":
        selected_region_id = json.load(request)['region_id']
        if selected_region_id:
            selected_region = Region.objects.get(id=selected_region_id)
            areas = Area.objects.filter(region=selected_region)

            context = {
                "areas": areas,
            }

        return render(request, 'components/areas_select.html', context)


def get_pickup_id(request):

    if request.method == "GET":
        region_name = "Nairobi"
        area_name = "CBD_PICKUP"
        area = Area.objects.filter(
            region__region=region_name, area=area_name).first()
        area_id = area.id

    return JsonResponse({"area_id": area_id})


@login_required(login_url='/accounts/signin/')
def update_address(request):
    user = request.user
    data = cart_data(request)
    cartItems = data['cartItems']

    try:
        address = Address.objects.get(customer=user.id)

        if request.method == "POST":
            form = AddressForm(request.POST, instance=address)

            if form.is_valid():
                form.save()

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))

                return redirect('customers:profile')

        form = AddressForm(instance=address)
        context = {'form': form,
                   "cartItems": cartItems, }
        return render(request, 'customers/update_address.html', context)

    except ObjectDoesNotExist:
        return redirect('customers:profile')


def get_shipping_cost(request):
    data = cart_data(request)
    cart = data['cart']

    if request.method == "POST":
        selected_area_id = json.load(request)['area_id']
        if selected_area_id:
            shipping_cost = ShippingCosts.objects.get(area=selected_area_id)
            if request.user.is_authenticated:
                shipping_n_cart_total = shipping_cost.cost + cart.get_cart_total
            else:
                shipping_n_cart_total = shipping_cost.cost + \
                    cart['get_cart_total']

            context = {
                "shipping_cost": shipping_cost.cost,
                "shipping_n_cart_total": str(shipping_n_cart_total),
            }
        data = {'rendered_total': render_to_string(
            'components/total_n_shipping.html', context)}

    return JsonResponse(data)


@login_required(login_url='/accounts/signin/')
def get_orders(request):
    # do an ajax request that will append all orders to this page
    # I will work on this once I refactor the cart app
    pass
