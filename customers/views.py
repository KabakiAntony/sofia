from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Address, Region, Customer
from .forms import AddressForm
from products.models import Product


@login_required(login_url='/accounts/signin/')
def user_profile(request):
    products = Product.objects.all()[:8]
    context = {"products":products}
    return render(request, "customers/profile.html", context)


@login_required(login_url='/accounts/signin/')
def get_user_infomation(request):
    user = request.user
    data = {}
    
    try:
        regions = Region.objects.all()
        address = Address.objects.get(customer__id=user.id)

        context =  {
            "customer": user.customer,
            "address":address,
        }
        data = {'customer': render_to_string('customers/customer_info.html', context, request)}

        return JsonResponse(data)

    except ObjectDoesNotExist:
        form = AddressForm()
        context = {
            "customer": user.customer,
            "regions": regions,
            "form":form,
        }

        data = {'customer': render_to_string('customers/add_address.html', context, request)}

        return JsonResponse(data)

    
@login_required(login_url='/accounts/signin/')
def add_address(request):
    if request.method == "POST":
        user = request.user
        form = AddressForm(request.POST)

        if form.is_valid():
            customer = Customer.objects.get(id=user.id)
            selected_region = form.cleaned_data.get('region')
            region = Region.objects.get(id=selected_region.id)

            mobile_no = form.cleaned_data.get('mobile_no')
            street = form.cleaned_data.get('street_lane_other')
            apartment = form.cleaned_data.get('apartment_suite_building')

            address = Address(
                customer=customer, 
                region=region,
                street_lane_other=street, 
                apartment_suite_building=apartment)
            address.save()

            customer.mobile_no = mobile_no
            customer.save()

            return redirect('customers:profile')

        else:
            for key in form.errors:
                messages.add_message(request, messages.ERROR, str(form.errors[key]))
    else:
        user = request.user
        form = AddressForm()
        context = {'form': form}

    return render(request, 'customers/profile.html', context)


@login_required(login_url='/accounts/signin/')
def get_orders(request):
    # do an ajax request that will append all orders to this page
    # I will work on this once I refactor the cart app
    pass


