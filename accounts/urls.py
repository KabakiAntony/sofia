from django.urls import path
from accounts.admin import admin_site
from .import views 

urlpatterns = [
    path('admin/', admin_site.urls, name="admin"),
    path('signup/', views.signup_user, name="signup"),
    path('signin/', views.signin_user, name="signin"),
    path('signout/', views.signout_user, name='signout'),
]
