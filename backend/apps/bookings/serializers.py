from rest_framework import serializers

from apps.cafes.serializers import CafeListSerializer

from .models import Reservation


class ReservationCreateSerializer(serializers.Serializer):
    cafe_id = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    guests = serializers.IntegerField(min_value=1)


class ReservationListSerializer(serializers.ModelSerializer):
    cafe = CafeListSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'cafe', 'date', 'time', 'guests', 'status', 'created_at')
