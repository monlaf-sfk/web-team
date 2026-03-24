from .models import Reservation


def get_user_reservations(*, user):
    return Reservation.objects.filter(user=user).select_related('cafe').order_by('-date', '-time')
