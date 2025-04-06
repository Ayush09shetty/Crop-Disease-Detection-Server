from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
class SellerManager(BaseUserManager):
    def create_seller(self, firstName, lastName, businessName, phone, email, gst, password=None):
        if not email:
            raise ValueError("Sellers must have an email")
        if not businessName:
            raise ValueError("Sellers must have a business name")

        email = self.normalize_email(email)
        seller = self.model(
            firstName=firstName,
            lastName=lastName,
            businessName=businessName,
            phone=phone,
            email=email,
            gst=gst,
        )
        seller.set_password(password)  # Hash password before storing
        seller.save(using=self._db)
        return seller

class Seller(AbstractBaseUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    businessName = models.CharField(max_length=100)
    phone = models.BigIntegerField(unique=True)
    email = models.EmailField(unique=True)
    gst = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    objects = SellerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'businessName', 'phone', 'gst']

    def __str__(self):
        return f"{self.businessName} ({self.firstName} {self.lastName} - {self.email})"
