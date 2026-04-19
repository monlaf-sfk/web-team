from django.contrib.auth import authenticate
from django.db.models import Avg, Count
from django.db.models.functions import Round
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from datetime import date, datetime, timedelta

from api.models import Badge, Cafe, Category, MenuItem, Mood, Reservation, Review
from api.serializers import (
    BadgeStatusSerializer,
    CafeSerializer,
    CafeStatsSerializer,
    CategorySerializer,
    HourBusynessSerializer,
    LoginSerializer,
    MenuItemSerializer,
    MoodSerializer,
    RegisterSerializer,
    ReservationSerializer,
    ReviewSerializer,
)


def cafes_queryset():
    return (
        Cafe.objects
        .select_related('category')
        .prefetch_related('moods')
        .annotate(
            avg_rating=Round(Avg('reviews__rating'), precision=1),
            reviews_count=Count('reviews', distinct=True),
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
        qs = cafes_queryset()
        moods = self.request.query_params.get('moods')
        if moods:
            slugs = [s for s in moods.split(',') if s]
            if slugs:
                qs = qs.filter(moods__slug__in=slugs).distinct()
        return qs


class MoodListAPIView(generics.ListAPIView):
    queryset = Mood.objects.all()
    serializer_class = MoodSerializer
    pagination_class = None


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


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cafe_stats(request):
    agg = Review.objects.aggregate(avg=Avg('rating'))
    data = {
        'cafes_count': Cafe.objects.count(),
        'reviews_count': Review.objects.count(),
        'reservations_count': Reservation.objects.count(),
        'avg_rating': round(agg['avg'], 2) if agg['avg'] is not None else None,
    }
    return Response(CafeStatsSerializer(data).data)


class LoginAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
        })


def _busyness_level(count, max_count):
    if max_count == 0 or count == 0:
        return 'empty'
    ratio = count / max_count
    if ratio < 0.34:
        return 'low'
    if ratio < 0.67:
        return 'medium'
    return 'high'


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def cafe_busyness(request, cafe_id):
    if not Cafe.objects.filter(pk=cafe_id).exists():
        return Response({'detail': 'Cafe not found.'}, status=status.HTTP_404_NOT_FOUND)

    rows = (
        Reservation.objects
        .filter(cafe_id=cafe_id)
        .values('time__hour')
        .annotate(count=Count('id'))
    )
    by_hour = {r['time__hour']: r['count'] for r in rows}
    max_count = max(by_hour.values(), default=0)

    hours = list(range(9, 23))
    data = [
        {
            'hour': h,
            'count': by_hour.get(h, 0),
            'level': _busyness_level(by_hour.get(h, 0), max_count),
        }
        for h in hours
    ]

    now = datetime.now()
    today = date.today()
    soon = (now + timedelta(hours=1)).time()
    live_count = Reservation.objects.filter(
        cafe_id=cafe_id,
        date=today,
        time__gte=now.time(),
        time__lte=soon,
    ).count()
    live_level = _busyness_level(live_count, max(max_count, 1))

    return Response({
        'hours': HourBusynessSerializer(data, many=True).data,
        'current': {'count': live_count, 'level': live_level, 'hour': now.hour},
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_badges(request):
    user = request.user
    reservations = Reservation.objects.filter(user=user).count()
    reviews = Review.objects.filter(user=user).count()
    categories = (
        Reservation.objects
        .filter(user=user)
        .values('cafe__category')
        .distinct()
        .count()
    )
    favorites = 0

    progress_map = {
        'reservations': reservations,
        'reviews': reviews,
        'categories': categories,
        'favorites': favorites,
    }

    badges = []
    earned_count = 0
    for b in Badge.objects.all():
        progress = progress_map.get(b.rule_type, 0)
        earned = progress >= b.threshold
        if earned:
            earned_count += 1
        badges.append({
            'slug': b.slug,
            'name': b.name,
            'emoji': b.emoji,
            'description': b.description,
            'threshold': b.threshold,
            'progress': min(progress, b.threshold),
            'earned': earned,
        })

    xp = reservations + reviews * 2
    level = xp // 5 + 1
    next_level_xp = level * 5

    return Response({
        'username': user.username,
        'level': level,
        'xp': xp,
        'next_level_xp': next_level_xp,
        'reservations': reservations,
        'reviews': reviews,
        'earned_count': earned_count,
        'total_count': len(badges),
        'badges': BadgeStatusSerializer(badges, many=True).data,
    })


class LogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        refresh = request.data.get('refresh')
        if not refresh:
            return Response(
                {'detail': 'refresh token is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            return Response(
                {'detail': 'Invalid or expired token.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_205_RESET_CONTENT)
