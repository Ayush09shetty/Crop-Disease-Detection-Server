from django.urls import path
from .views import ConsultantRegisterView, ConsultantLoginView, ConsultantProfileView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("signup/", ConsultantRegisterView.as_view(), name="consultant_register"),
    path("login/", ConsultantLoginView.as_view(), name="consultant_login"),
    path("profile/<slug:consultant_id>", ConsultantProfileView.as_view(), name="consultant_profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
