from django.db import models
from django.conf import settings

from helpers import TimestampAbstractModel


CustomUser = settings.AUTH_USER_MODEL


class Customer(TimestampAbstractModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer")

    def __str__(self):
        return f"{self.user.email} - Customer"
