from django.contrib import admin
from django.urls import path
from productmodule import views

urlpatterns = [
    path('addproducts/', views.add_product),
    path('listproducts/', views.list_products),
    path('updateproduct/<int:pk>/', views.update_product, name='update_product'),
    path('product/<int:pk>/', views.get_product_by_id, name='get_product_by_id'),
    #path('products/category/', views.get_products_by_category, name='get_products_by_category'),
    path('category/<str:category>/', views.get_products_by_category, name='get_products_by_category'),

]