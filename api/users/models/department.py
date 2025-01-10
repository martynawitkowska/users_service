from django.db import models

from helpers import TimestampAbstractModel

from .organization import Organization


class Department(TimestampAbstractModel):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name
