from django.urls import path

from .views import CafeDetailView, CafeListView, CategoryDetailView, CategoryListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('cafes/', CafeListView.as_view(), name='cafe-list'),
    path('cafes/<int:pk>/', CafeDetailView.as_view(), name='cafe-detail'),
]
