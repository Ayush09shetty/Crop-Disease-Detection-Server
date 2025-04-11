from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('productmodule.urls')),
    path('hero/', include('templatehero.urls')),
    path("prom/", include('promotion.urls')),
    path("user/", include('user.urls')),
    path("seller/", include('seller.urls')),
    path("cart/", include('Cart.urls')),
    path("profile/", include('Profile.urls')),
    path("consultant/", include('Consultant.urls')),
    path("appointment/", include('Appointments.urls')),
    path("checkout/", include('Checkout.urls')),
    path("search/", include('SearchHistory.urls')),
    path("predict/", include('PredectModel.urls')),
]
