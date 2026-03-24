from django.conf import settings
from django.db import models

from apps.cafes.models import Cafe
from apps.common.models import BaseModel


class Reservation(BaseModel):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations'
    )
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name='reservations'
    )
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    def __str__(self):
        return f'{self.user} — {self.cafe} ({self.date})'
