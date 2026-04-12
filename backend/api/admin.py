from django.contrib import admin

from api.models import Cafe, Category, MenuItem, Reservation, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'address')
    list_filter = ('category',)
    search_fields = ('name', 'address')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cafe', 'price')
    list_filter = ('cafe',)
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cafe', 'rating', 'created_at')
    list_filter = ('cafe', 'rating')
    search_fields = ('user__username', 'cafe__name')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'cafe', 'date', 'time', 'guests')
    list_filter = ('date', 'cafe')
    search_fields = ('user__username', 'cafe__name')
