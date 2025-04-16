from django.urls import path
from .views import ping, predict, video_predict, set_disease

urlpatterns = [
    path('ping/', ping),
    path('predict/', predict),
    path('video-predict/', video_predict),
    path('set-disease/', set_disease)  
]
