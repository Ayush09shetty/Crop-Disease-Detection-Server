from django.urls import path
from promotion import views

urlpatterns = [
    path('upload_promotion/', views.upload_promotion_image, name='upload_promotion_image'),
    path('get-images/', views.get_random_promotion_image_path, name='get_promotion_images'),
]
