from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import serializers

from api.models import Cafe, Category, MenuItem, Reservation, Review

User = get_user_model()

MIN_GUESTS = 1
MAX_GUESTS = 20


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'cafe', 'name', 'price')


class CafeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
    )
    avg_rating = serializers.FloatField(read_only=True, default=None)
    reviews_count = serializers.IntegerField(read_only=True, default=0)

    class Meta:
        model = Cafe
        fields = (
            'id', 'name', 'address', 'description', 'image',
            'category', 'category_id', 'opens_at', 'closes_at',
            'avg_rating', 'reviews_count',
        )


class ReservationSerializer(serializers.ModelSerializer):
    cafe_name = serializers.CharField(source='cafe.name', read_only=True)

    class Meta:
        model = Reservation
        fields = ('id', 'cafe', 'cafe_name', 'date', 'time', 'guests', 'created_at')
        read_only_fields = ('created_at',)

    def validate_date(self, value):
        if value < date.today():
            raise serializers.ValidationError('Date cannot be in the past.')
        return value

    def validate_guests(self, value):
        if value < MIN_GUESTS or value > MAX_GUESTS:
            raise serializers.ValidationError(
                f'Guests must be between {MIN_GUESTS} and {MAX_GUESTS}.'
            )
        return value

    def validate(self, attrs):
        cafe = attrs.get('cafe')
        t = attrs.get('time')
        if cafe and t:
            opens = cafe.opens_at
            closes = cafe.closes_at
            if opens <= closes:
                in_hours = opens <= t <= closes
            else:
                in_hours = t >= opens or t <= closes
            if not in_hours:
                raise serializers.ValidationError(
                    {'time': f'Cafe works from {opens.strftime("%H:%M")} to {closes.strftime("%H:%M")}.'}
                )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'cafe', 'username', 'rating', 'text', 'created_at')
        read_only_fields = ('cafe', 'created_at')

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
