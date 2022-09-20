from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from .models import User,Customer
from cart.utils import cart_data


def signup_user(request):
    form = MyUserCreationForm()
    data = cart_data(request)
    cartItems = data['cartItems']
    

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            name = " ".join([first_name, last_name])
            Customer.objects.create(user=user,name=name,email=email)

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'accounts/signup.html', context)

def signin_user(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    # later in dev add a next link to always take the user back to the
    # view that required him to be logged in.
    if request.user.is_authenticated:
        # we don't  want users relogin in again
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 
                "Email and or password is not correct, please check and try again.")

        except:
            messages.error(request, 
            'User account could not be found, please signup to continue.')
        
    context = {'cartItems':cartItems}
    return render(request, 'accounts/signin.html', context)

def signout_user(request):
    logout(request)
    return redirect('home')