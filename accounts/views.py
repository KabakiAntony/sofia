from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from .models import User


def signup_user(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {'form': form }
    return render(request, 'accounts/signup.html', context)

def signin_user(request):
    # later in dev add a next link to always the user back to the
    # view that required him to be logged in.
    if request.user.is_authenticated:
        # we don't  want users relogin in again
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User not found.')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Email and or password is not correct")

    context = {}
    return render(request, 'accounts/signin.html', context)

def signout_user(request):
    logout(request)
    return redirect('home')