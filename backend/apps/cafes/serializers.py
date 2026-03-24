from rest_framework import serializers

from .models import Cafe, Category, MenuItem


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image')


class CafeListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)

    class Meta:
        model = Cafe
        fields = ('id', 'name', 'address', 'image', 'is_popular', 'category')


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('id', 'name', 'description', 'price', 'is_available')


class CafeDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    menu_items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cafe
        fields = ('id', 'name', 'description', 'address', 'phone', 'image', 'is_popular', 'category', 'menu_items')
