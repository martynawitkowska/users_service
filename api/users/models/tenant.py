from django.db import models

from helpers import TimestampAbstractModel


class Tenant(TimestampAbstractModel):
    name = models.CharField(max_length=255, unique=True)
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

