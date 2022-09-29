from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import MyUserCreationForm
from .models import User,Customer
from cart.utils import cart_data
from journaling.emails import send_email
from journaling.tokens import account_activation_token


def signup_user(request):
    form = MyUserCreationForm()
    data = cart_data(request)
    cartItems = data['cartItems']
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')

            name = " ".join([first_name, last_name])
            Customer.objects.create(user=user,name=name,email=email)

            # send activation email instead of signing the user in.
            current_site = get_current_site(request)
            protocol = request.scheme
            email_subject = f""" Welcome and verfiy your email."""
            email_content = render_to_string("accounts/verify_email.html",{
                'user':user,
                'current_site':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                "protocol":protocol
            })
            
            try:
                send_email(request, email, email_subject, email_content)
                return  render(request, 'accounts/check_email.html', {'cartItems':cartItems})
                
            except Exception as e:
                messages.add_message(request, messages.ERROR, str(e))
        else:
            for key in form.errors:
                messages.add_message(request, messages.ERROR, str(form.errors[key]))
               
    context = {'form': form, 'cartItems':cartItems}
    return render(request, 'accounts/signup.html', context)

def signin_user(request):
    data = cart_data(request)
    cartItems = data['cartItems']

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            if not user.email_confirmed:
                messages.add_message(request, messages.ERROR, 
                "You have not verified your email, headover to your email inbox \
                    click on the verify email link.")
            else:
                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.add_message(request, messages.ERROR, 
                    "Email and or password is not correct, please check and try again.")

        except:
            messages.add_message(request, messages.ERROR, 
                "User account could not be found, please signup to continue.")
            
        
    context = {'cartItems':cartItems}
    return render(request, 'accounts/signin.html', context)

def verify_email(request, uidb64, token):
    """ verify email """
    data = cart_data(request)
    cartItems = data['cartItems']
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
    else:
        error_message = 'Account activation link is invalid.'
        context = {'cartItems':cartItems, "message": error_message}
        return render(request, 'accounts/verification_failed.html', context)

    return redirect('home')

def signout_user(request):
    logout(request)
    return redirect('home')

