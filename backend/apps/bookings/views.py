from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_user_reservations
from .serializers import ReservationCreateSerializer, ReservationListSerializer
from .services import cancel_reservation, create_reservation


class ReservationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = get_user_reservations(user=request.user)
        serializer = ReservationListSerializer(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReservationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = create_reservation(user=request.user, **serializer.validated_data)
        return Response(
            ReservationListSerializer(reservation).data,
            status=status.HTTP_201_CREATED,
        )


class ReservationCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        reservation = cancel_reservation(user=request.user, reservation_id=pk)
        return Response(ReservationListSerializer(reservation).data)
