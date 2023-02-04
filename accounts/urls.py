from django.urls import path
from .import views 

urlpatterns = [

    path('signup/', views.signup_user, name="signup"),
    path('signin/', views.signin_user, name="signin"),
    path('signout/', views.signout_user, name='signout'),
    path('verify/<uidb64>/<token>/', views.verify_email, name='verify'),
    path('forgot/', views.send_reset_link, name='forgot' ),
    path('change/<uidb64>/<token>/', views.change_password, name='change'),
]
