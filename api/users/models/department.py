from django.db import models

from .organization import Organization
from helpers import TimestampAbstractModel


class Department(TimestampAbstractModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name