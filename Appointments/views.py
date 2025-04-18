from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Appointment
from .serializers import AppointmentSerializer
from Consultant.models import ConsultantUser
from Consultant.serializers import ConsultantUserSerializer  # Ensure you have this serializer

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request):
        user = request.user
        data = request.data

        consultant_id = data.get("consultantId")
        mode = data.get("mode").lower()  
        date = data.get("date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        if not all([consultant_id, mode, date, start_time, end_time]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if mode not in ["online", "offline"]:
            return Response({"error": "Invalid mode. Choose 'online' or 'offline'."}, status=status.HTTP_400_BAD_REQUEST)

        consultant = get_object_or_404(ConsultantUser, id=consultant_id)

        if start_time >= end_time:
            return Response({"error": "Start time must be before end time"}, status=status.HTTP_400_BAD_REQUEST)

        overlapping_appointments = Appointment.objects.filter(
            consultant=consultant, 
            date=date
        ).filter(
            start_time__lt=end_time, 
            end_time__gt=start_time
        )

        if overlapping_appointments.exists():
            return Response({"error": "Time slot already booked, please choose another time."}, status=status.HTTP_400_BAD_REQUEST)

        appointment = Appointment.objects.create(
            user=user,
            consultant=consultant,
            mode=mode,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        serializer = AppointmentSerializer(appointment)
        return Response({"message": "Appointment booked successfully!", "appointment": serializer.data}, status=status.HTTP_201_CREATED)


class UpdateAppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        data = request.data
        appointment_id = data.get("appointmentId")
        new_status = data.get("status").lower()  

        if not appointment_id or not new_status:
            return Response({"error": "Appointment ID and status are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in ["pending", "confirmed", "cancelled"]:
            return Response({"error": "Invalid status. Allowed values: 'pending', 'confirmed', 'cancelled'."}, status=status.HTTP_400_BAD_REQUEST)

        appointment = get_object_or_404(Appointment, id=appointment_id)

        if request.user != appointment.consultant and request.user != appointment.user:
            return Response({"error": "You are not authorized to update this appointment."}, status=status.HTTP_403_FORBIDDEN)

        appointment.status = new_status
        appointment.save()

        return Response({"message": "Appointment status updated successfully!", "new_status": new_status}, status=status.HTTP_200_OK)


class GetBookedSlotsView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        data = request.data
        consultant_id = data.get("consultantId")
        date = data.get("date")

        if not consultant_id or not date:
            return Response({"error": "Consultant ID and date are required"}, status=status.HTTP_400_BAD_REQUEST)

        consultant = get_object_or_404(ConsultantUser, id=consultant_id)

        booked_slots = Appointment.objects.filter(consultant=consultant, date=date).values("start_time", "end_time")

        return Response({"consultantId": consultant_id, "date": date, "booked_slots": list(booked_slots)}, status=status.HTTP_200_OK)


class GetConsultantListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        consultants = ConsultantUser.objects.all()
        serializer = ConsultantUserSerializer(consultants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetConsultantByIdView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request, consultant_id):
        consultant = get_object_or_404(ConsultantUser, id=consultant_id)
        serializer = ConsultantUserSerializer(consultant)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        appointments = Appointment.objects.filter(user=user).order_by("date", "start_time")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConsultantAppointmentsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, consultant_id):
        consultant = get_object_or_404(ConsultantUser, id=consultant_id)
        
        if request.user != consultant:
            return Response({"error": "Unauthorized to view this consultant's appointments"}, status=status.HTTP_403_FORBIDDEN)

        appointments = Appointment.objects.filter(consultant=consultant).order_by("date", "start_time")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
