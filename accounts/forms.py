from .models import User
from django import forms
from django.contrib.auth.forms import(
    UserCreationForm, PasswordResetForm, SetPasswordForm
) 


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class UserForgotPasswordForm(PasswordResetForm):
    """ user forgot password form"""
    email = forms.EmailField(label='Email address',
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class':'email-address',
                'placeholder': 'xyz@zyx.com',
                "type":'email',
                'id': 'email_address'
            }))


class UserSetNewPasswordForm(SetPasswordForm):
    """" set new password """
    new_password1 = forms.CharField(label='Password',
        help_text='<span class="error-span" id="password-error">Your password cant be too similar.</span>',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                "type":'password',
                'id':'password_one',
            }))

    new_password2 = forms.CharField(label='Password',
        help_text=False,
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'password',
                "type":'password',
                'id':'password_two',
            }))
