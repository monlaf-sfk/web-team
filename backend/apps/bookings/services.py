from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.cafes.models import Cafe
from apps.common.exceptions import ApplicationError

from .models import Reservation


def create_reservation(*, user, cafe_id, date, time, guests):
    if date < timezone.now().date():
        raise ApplicationError('Cannot book for a past date.')

    cafe = get_object_or_404(Cafe, id=cafe_id)

    return Reservation.objects.create(
        user=user,
        cafe=cafe,
        date=date,
        time=time,
        guests=guests,
    )


def cancel_reservation(*, user, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=user)

    if reservation.status == Reservation.Status.CANCELLED:
        raise ApplicationError('Reservation is already cancelled.')

    reservation.status = Reservation.Status.CANCELLED
    reservation.save(update_fields=['status', 'updated_at'])
    return reservation
