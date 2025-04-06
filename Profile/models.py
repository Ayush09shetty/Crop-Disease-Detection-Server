from django.conf import settings
from django.db import models
import uuid

class UserAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    line_one = models.CharField(max_length=50)
    line_two = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=20, default="India")
    zip_code = models.PositiveIntegerField()
