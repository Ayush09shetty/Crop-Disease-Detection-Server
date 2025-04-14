from django.urls import path
from .views import ping, predict,video_predict

urlpatterns = [
    path('ping/', ping),
    path('predict/', predict),
    path('video-predict/', video_predict)  
]
