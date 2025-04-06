from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.conf import settings

class UserManager(BaseUserManager):
    def create_user(self, phone, firstName, lastName, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(phone=phone, firstName=firstName, lastName=lastName)
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_admin(self, phone, firstName, lastName, password=None):
        user = self.create_user(phone, firstName, lastName, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.BigIntegerField(unique=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.phone})"

    @property
    def is_staff(self):
        return self.is_admin  # Admins can access Django admin panel if needed
