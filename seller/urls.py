from django.urls import path
from .views import seller_signup, seller_login, seller_profile,get_seller_id_from_token

urlpatterns = [
    path('signup/', seller_signup, name='seller_signup'),
    path('login/', seller_login, name='seller_login'),
    path('profile/<slug:seller_id>/', seller_profile, name='seller_profile'),
    path('id/', get_seller_id_from_token, name='get_seller_id_from_token')
]
