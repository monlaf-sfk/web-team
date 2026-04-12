from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import (
    CafeDetailAPIView,
    CafeListAPIView,
    CafeReviewListAPIView,
    CategoryDetailAPIView,
    CategoryListAPIView,
    MenuItemDetailAPIView,
    MenuItemListAPIView,
    ReservationDetailAPIView,
    ReservationListAPIView,
    ReviewDetailAPIView,
    register,
)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:category_id>/', CategoryDetailAPIView.as_view()),

    path('cafes/', CafeListAPIView.as_view()),
    path('cafes/<int:cafe_id>/', CafeDetailAPIView.as_view()),
    path('cafes/<int:cafe_id>/reviews/', CafeReviewListAPIView.as_view()),

    path('menu-items/', MenuItemListAPIView.as_view()),
    path('menu-items/<int:menu_item_id>/', MenuItemDetailAPIView.as_view()),

    path('reservations/', ReservationListAPIView.as_view()),
    path('reservations/<int:reservation_id>/', ReservationDetailAPIView.as_view()),

    path('reviews/<int:review_id>/', ReviewDetailAPIView.as_view()),

    path('register/', register),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
