from django.db.models import Avg, Count, IntegerField
from django.db.models.functions import Round
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.models import Cafe, Category, MenuItem, Reservation, Review
from api.serializers import (
    CafeSerializer,
    CategorySerializer,
    MenuItemSerializer,
    RegisterSerializer,
    ReservationSerializer,
    ReviewSerializer,
)


def cafes_queryset():
    return (
        Cafe.objects
        .select_related('category')
        .annotate(
            avg_rating=Round(Avg('reviews__rating'), precision=1),
            reviews_count=Count('reviews'),
        )
    )


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = 'category_id'


class CafeListAPIView(generics.ListCreateAPIView):
    serializer_class = CafeSerializer
    filterset_fields = ('category',)
    search_fields = ('name', 'address', 'description')
    ordering_fields = ('name', 'avg_rating')
    ordering = ('name',)

    def get_queryset(self):
        return cafes_queryset()


class CafeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CafeSerializer
    lookup_url_kwarg = 'cafe_id'

    def get_queryset(self):
        return cafes_queryset()


class MenuItemListAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    filterset_fields = ('cafe',)

    def get_queryset(self):
        return MenuItem.objects.all()


class MenuItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    lookup_url_kwarg = 'menu_item_id'


class ReservationListAPIView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('cafe')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationDetailAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'reservation_id'

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).select_related('cafe')


class CafeReviewListAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Review.objects.filter(cafe_id=self.kwargs['cafe_id']).select_related('user')

    def perform_create(self, serializer):
        cafe_id = self.kwargs['cafe_id']
        if Review.objects.filter(user=self.request.user, cafe_id=cafe_id).exists():
            raise ValidationError({'detail': 'You have already reviewed this cafe.'})
        serializer.save(user=self.request.user, cafe_id=cafe_id)


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = 'review_id'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).select_related('user', 'cafe')


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
