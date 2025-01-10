from django.conf import settings
from django.db import models

from helpers import TimestampAbstractModel

from .department import Department

CustomUser = settings.AUTH_USER_MODEL


class Customer(TimestampAbstractModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='customers')

    def __str__(self):
        return f"{self.user.email} - Customer"

