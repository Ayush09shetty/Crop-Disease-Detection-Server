from django.contrib import admin
from django.urls import path
from productmodule import views
from .views import UpdateOrderStatusView,AllOrderStatusView,UpdateInventoryView,GetAllInventoryView,recent_products

urlpatterns = [
    path('addproducts/', views.add_product),
    path('listproducts/', views.list_products),
    path('updateproduct/<slug:pk>/', views.update_product, name='update_product'),
    path('product/<slug:pk>/', views.get_product_by_id, name='get_product_by_id'),
    #path('products/category/', views.get_products_by_category, name='get_products_by_category'),
    path('category/<str:category>/', views.get_products_by_category, name='get_products_by_category'),
    path('UpdateOrderStatusView/<slug:order_id>', UpdateOrderStatusView.as_view(), name='update_order_status'),
    path('all-order-status/', AllOrderStatusView.as_view(), name='all_order_status'),
    path('update-inventory/<slug:product_id>/', UpdateInventoryView.as_view(), name='update_inventory'),
    path('GetAllInventoryView/', GetAllInventoryView.as_view(), name='get_all_inventory'),
    path('recent_products/', recent_products, name='recent_products'),
]