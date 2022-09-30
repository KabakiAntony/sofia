from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import MyUserCreationForm, UserSetNewPasswordForm, UserForgotPasswordForm
from .models import User,Customer
from cart.utils import cart_data
from journaling.emails import send_email
from journaling.tokens import account_activation_token, password_reset_token


def signup_user(request):
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
    
    else:
        form = MyUserCreationForm()
        data = cart_data(request)
        cartItems = data['cartItems']

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


def send_reset_link(request):
    """ view for sending password reset link """
    data = cart_data(request)
    cartItems = data['cartItems']

    if request.method == "POST":
        form = UserForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_query_set = User.objects.filter(email=email)
            current_site = get_current_site(request)
            protocol = request.scheme

            if len(user_query_set) > 0:
                user = user_query_set[0]
                user.is_active = False
                user.reset_password = True
                user.save()

                email_subject = f""" Password reset link."""
                email_content = render_to_string("accounts/password_reset_req_email_body.html",{
                    'user':user,
                    'current_site':current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':password_reset_token.make_token(user),
                    "protocol":protocol
                })
                
                try:
                    send_email(request, email, email_subject, email_content)
                except Exception as e:
                    # if for some reason the email was not sent
                    print(str(e))

            message = "If this email is know to us, an email will be sent to your account shortly."
            messages.add_message(request, messages.SUCCESS, f'Email {email} submitted successfully')

        else:
            messages.add_message(request, messages.WARNING, "Email was not submitted")
            return render(request, 'accounts/password_reset_email_form.html', {'form': form, 'cartItems':cartItems})
    
    context = {
            'cartItems':cartItems,
            'form': UserForgotPasswordForm
        }
    return render(request, 'accounts/password_reset_email_form.html', context)


def change_password(request, uidb64, token):
    """ view for reseting password """
    data = cart_data(request)
    cartItems = data['cartItems']

    if request.method == 'POST':
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = UserSetNewPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                user.is_active = True
                user.reset_password = False
                user.save()
                messages.add_message(request, messages.SUCCESS, "Password reset successfully.")
                return redirect('signin')
            else:
                context = {
                    'form': form,
                    'uid':uidb64,
                    'token':token,
                    'cartItems':cartItems,
                }
                messages.add_message(request, messages.WARNING, "Password could not be reset")
                return render(request, 'accounts/new_password_form.html', context)
        else:
            messages.add_message(request, messages.WARNING,
                "Password reset link is invalid, please request for a new one, here.")
    
    # this case caters for GET part of this view
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        context = {
                    'form':UserSetNewPasswordForm(user),
                    'uid':uidb64,
                    'token':token,
                    'cartItems':cartItems,
                }
        return render(request, 'accounts/new_password_form.html', context)
    else:
        messages.add_message(request, messages.WARNING,
                "Password reset link is invalid, please request for a new one, here.")
    
    return redirect('forgot')


def signout_user(request):
    logout(request)
    return redirect('home')

