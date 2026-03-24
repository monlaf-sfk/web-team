from django.urls import path

from .views import ReservationCancelView, ReservationListCreateView

urlpatterns = [
    path('', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('<int:pk>/cancel/', ReservationCancelView.as_view(), name='reservation-cancel'),
]
