from django.urls import path
from .views import get_random_hero_images, upload_hero_image

urlpatterns = [
    path('random-hero-images/', get_random_hero_images, name='random_hero_images'),
    path('upload-hero-image/', upload_hero_image, name='upload_hero_image'),
]
