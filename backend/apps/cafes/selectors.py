from .models import Cafe, Category


def get_categories():
    return Category.objects.all()


def get_category_by_slug(*, slug):
    return Category.objects.get(slug=slug)


def get_cafes(*, popular=None):
    qs = Cafe.objects.select_related('category')
    if popular:
        qs = qs.filter(is_popular=True)
    return qs


def get_cafe_detail(*, cafe_id):
    return Cafe.objects.prefetch_related('menu_items').select_related('category').get(id=cafe_id)
