from django.urls import path
from .views import ping, predict

urlpatterns = [
    path('ping/', ping),
    path('predict/', predict),
]
