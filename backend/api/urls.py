from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    CafeDetailAPIView,
    CafeListAPIView,
    CafeReviewListAPIView,
    CategoryDetailAPIView,
    CategoryListAPIView,
    LoginAPIView,
    LogoutAPIView,
    MenuItemDetailAPIView,
    MenuItemListAPIView,
    MoodListAPIView,
    ReservationDetailAPIView,
    ReservationListAPIView,
    ReviewDetailAPIView,
    cafe_busyness,
    cafe_stats,
    my_badges,
    register,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view()),

    path('cafes/', CafeListAPIView.as_view()),
    path('cafes/<int:cafe_id>/', CafeDetailAPIView.as_view()),
    path('cafes/<int:cafe_id>/reviews/', CafeReviewListAPIView.as_view()),
    path('cafes/<int:cafe_id>/busyness/', cafe_busyness),

    path('moods/', MoodListAPIView.as_view()),

    path('menu-items/', MenuItemListAPIView.as_view()),
    path('menu-items/<int:menu_item_id>/', MenuItemDetailAPIView.as_view()),

    path('reservations/', ReservationListAPIView.as_view()),
    path('reservations/<int:reservation_id>/', ReservationDetailAPIView.as_view()),

    path('reviews/<int:review_id>/', ReviewDetailAPIView.as_view()),

    path('stats/', cafe_stats),
    path('me/badges/', my_badges),
    path('register/', register),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
