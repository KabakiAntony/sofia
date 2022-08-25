from django.urls import path
from .import views 

urlpatterns = [
    path('signup/', views.signup_user, name="signup"),
    path('signin/', views.signin_user, name="signin"),
    path('signout/', views.signout_user, name='signout'),
]
