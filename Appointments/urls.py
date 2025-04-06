from django.urls import path
from .views import BookAppointmentView,UpdateAppointmentStatusView,GetBookedSlotsView,GetConsultantListView,GetConsultantByIdView,UserAppointmentsView,ConsultantAppointmentsView

urlpatterns = [
    path("book/", BookAppointmentView.as_view(), name="book_appointment"),
    path("update-status/", UpdateAppointmentStatusView.as_view(), name="update_appointment_status"),
    path("get-booked-slots/", GetBookedSlotsView.as_view(), name="get_booked_slots"),
    path("consultant-list/", GetConsultantListView.as_view(), name="consultant_list"),
    path("consultant/<slug:consultant_id>/", GetConsultantByIdView.as_view(), name="consultant_detail"),
    path("user-appointments/", UserAppointmentsView.as_view(), name="user_appointments"),
    path("consultant-appointments/<uuid:consultant_id>/", ConsultantAppointmentsView.as_view(), name="consultant_appointments"),

]
