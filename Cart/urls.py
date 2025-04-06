from django.urls import path
from .views import AddToCartView, UpdateCartItemView, ViewCartView, DeleteCartItemView

urlpatterns = [
    path("add/", AddToCartView.as_view(), name="add_to_cart"),
    path("update/", UpdateCartItemView.as_view(), name="update_cart_item"),
    path("view/", ViewCartView.as_view(), name="view_cart"),
    path("delete/", DeleteCartItemView.as_view(), name="delete_cart_item"),
]
