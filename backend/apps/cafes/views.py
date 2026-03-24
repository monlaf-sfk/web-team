from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import get_cafe_detail, get_cafes, get_categories, get_category_by_slug
from .serializers import CafeDetailSerializer, CafeListSerializer, CategoryListSerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = get_categories()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailView(APIView):
    def get(self, request, slug):
        category = get_category_by_slug(slug=slug)
        cafes = get_cafes(popular=None).filter(category=category)
        serializer = CafeListSerializer(cafes, many=True)
        return Response(serializer.data)


class CafeListView(APIView):
    def get(self, request):
        popular = request.query_params.get('popular')
        cafes = get_cafes(popular=popular)
        serializer = CafeListSerializer(cafes, many=True)
        return Response(serializer.data)


class CafeDetailView(APIView):
    def get(self, request, pk):
        cafe = get_cafe_detail(cafe_id=pk)
        serializer = CafeDetailSerializer(cafe)
        return Response(serializer.data)
