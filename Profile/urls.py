from django.urls import path
from .views import AddAddressView, FetchAllAddressesView, UpdateAddressView,DeleteAddressView, UpdateUserPhoneView, UpdateUserNameView, UpdateUserPasswordView

urlpatterns = [
    path("add/", AddAddressView.as_view(), name="add_address"),
    path("all/", FetchAllAddressesView.as_view(), name="fetch_addresses"),
    path("update/", UpdateAddressView.as_view(), name="update_address"),
    path("delete/", DeleteAddressView.as_view(), name="delete_address"),
    path("update_phone/", UpdateUserPhoneView.as_view(), name="update_user_phone"),
    path("update_name/", UpdateUserNameView.as_view(), name="update_user_name"),
    path("update_password/", UpdateUserPasswordView.as_view(), name="update_user_password"),
]
