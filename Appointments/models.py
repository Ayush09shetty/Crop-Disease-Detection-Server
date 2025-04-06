from django.conf import settings  # Import settings for user model
from django.db import models
import uuid
from Consultant.models import ConsultantUser  # Correct import for ConsultantUser

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Fix user relation
    consultant = models.ForeignKey(ConsultantUser, on_delete=models.CASCADE)  # Correct consultant relation
    mode = models.CharField(max_length=7, choices=[("online", "Online"), ("offline", "Offline")])
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="pending",
    )

    def __str__(self):
        return f"Appointment with {self.consultant} on {self.date}"
