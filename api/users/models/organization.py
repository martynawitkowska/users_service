from django.db import models

from .tenant import Tenant
from helpers import TimestampAbstractModel


class Organization(TimestampAbstractModel):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="organizations")

    def __str__(self):
        return self.name