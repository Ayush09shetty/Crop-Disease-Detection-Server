from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "user", "consultant", "mode", "date", "start_time", "end_time", "status"]
        read_only_fields = ["id", "user", "status"]  # User and status should not be updated manually
