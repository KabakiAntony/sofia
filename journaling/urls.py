from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .admin import journaling_admin_site
from django.urls import path, include
from products import views as home_page

urlpatterns = [
    path('admin/', journaling_admin_site.urls),
    path('accounts/', include('accounts.urls')), 
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('customers/', include('customers.urls')),
    path('orders/', include('orders.urls')),
    path('', home_page.home, name='home'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
