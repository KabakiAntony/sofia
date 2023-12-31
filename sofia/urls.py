from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .admin import sofia_admin_site
from django.urls import path, include

urlpatterns = [
    path('admin/', sofia_admin_site.urls),
    path('__debug__/', include("debug_toolbar.urls")),
    path('', include('accounts.urls')),
    path('', include('cart.urls')),
    path('', include('customers.urls')),
    path('', include('products.urls')),
    path('', include('orders.urls')),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
