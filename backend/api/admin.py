from django.contrib import admin

from api.models import Badge, Cafe, Category, MenuItem, Mood, Reservation, Review


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'rule_type', 'threshold')
    search_fields = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'slug', 'name', 'emoji')
    search_fields = ('name', 'slug')


@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'address')
    list_filter = ('category', 'moods')
    search_fields = ('name', 'address')
    filter_horizontal = ('moods',)


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
