from django.core.management.base import BaseCommand

from api.models import Badge, Cafe, Category, MenuItem, Mood


CATEGORIES = [
    'Coffee Shops',
    'Italian',
    'Kazakh',
    'Japanese',
    'Fast Food',
]

MOODS = [
    ('work', 'Work-friendly', '💻'),
    ('date', 'Date night', '❤️'),
    ('friends', 'With friends', '👥'),
    ('photo', 'Instagrammable', '📸'),
]

BADGES = [
    ('first-visit', 'Newbie', '🌱', 'Make your first reservation', 'reservations', 1),
    ('frequent', 'Frequent Guest', '🔥', 'Book 5 reservations', 'reservations', 5),
    ('regular', 'Regular', '👑', 'Book 15 reservations', 'reservations', 15),
    ('critic', 'Critic', '✍️', 'Leave 3 reviews', 'reviews', 3),
    ('coffee-expert', 'Coffee Expert', '☕', 'Leave 10 reviews', 'reviews', 10),
    ('explorer', 'Explorer', '🧭', 'Visit 3 different categories', 'categories', 3),
]

CAFES = [
    {
        'name': 'Cozy Corner',
        'address': 'Almaty, Abay 10',
        'description': 'A warm cozy coffee shop with homemade pastries.',
        'image': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800',
        'category': 'Coffee Shops',
        'opens_at': '07:30', 'closes_at': '21:00',
        'moods': ['work', 'date'],
        'menu': [('Cappuccino', 1200), ('Latte', 1300), ('Croissant', 800)],
    },
    {
        'name': 'Latte Art',
        'address': 'Almaty, Nazarbayev 15',
        'description': 'Specialty coffee and desserts in the city center.',
        'image': 'https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=800',
        'category': 'Coffee Shops',
        'opens_at': '08:00', 'closes_at': '23:00',
        'moods': ['work', 'photo'],
        'menu': [('Flat White', 1400), ('Espresso', 900), ('Cheesecake', 1600)],
    },
    {
        'name': 'Pasta House',
        'address': 'Almaty, Dostyk 5',
        'description': 'Authentic Italian pasta and wood-fired pizza.',
        'image': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
        'category': 'Italian',
        'opens_at': '11:00', 'closes_at': '23:30',
        'moods': ['date', 'friends'],
        'menu': [('Spaghetti Carbonara', 2500), ('Margherita Pizza', 2800), ('Tiramisu', 1500)],
    },
    {
        'name': 'Bella Roma',
        'address': 'Almaty, Al-Farabi 77',
        'description': 'Family-friendly Italian restaurant.',
        'image': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=800',
        'category': 'Italian',
        'opens_at': '12:00', 'closes_at': '23:00',
        'moods': ['friends', 'date'],
        'menu': [('Lasagna', 2700), ('Fettuccine Alfredo', 2400), ('Panna Cotta', 1400)],
    },
    {
        'name': 'Dastarkhan',
        'address': 'Almaty, Tole Bi 50',
        'description': 'Traditional Kazakh cuisine in a cozy setting.',
        'image': 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800',
        'category': 'Kazakh',
        'opens_at': '10:00', 'closes_at': '22:00',
        'moods': ['friends'],
        'menu': [('Beshbarmak', 3500), ('Manty', 2000), ('Baursak', 600)],
    },
    {
        'name': 'Sakura',
        'address': 'Almaty, Satpayev 22',
        'description': 'Fresh sushi and ramen by a Japanese chef.',
        'image': 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800',
        'category': 'Japanese',
        'opens_at': '12:00', 'closes_at': '22:30',
        'moods': ['date', 'photo'],
        'menu': [('Philadelphia Roll', 3200), ('Tonkotsu Ramen', 3500), ('Miso Soup', 900)],
    },
    {
        'name': 'Burger Town',
        'address': 'Almaty, Furmanov 22',
        'description': 'Juicy burgers and crispy fries.',
        'image': 'https://images.unsplash.com/photo-1561758033-d89a9ad46330?w=800',
        'category': 'Fast Food',
        'opens_at': '10:00', 'closes_at': '02:00',
        'moods': ['friends'],
        'menu': [('Cheeseburger', 1800), ('Double Beef Burger', 2400), ('French Fries', 700)],
    },
]


class Command(BaseCommand):
    help = 'Seed the database with demo categories, cafes and menu items.'

    def handle(self, *args, **options):
        MenuItem.objects.all().delete()
        Cafe.objects.all().delete()
        Category.objects.all().delete()
        Mood.objects.all().delete()
        Badge.objects.all().delete()

        for slug, name, emoji, desc, rule, threshold in BADGES:
            Badge.objects.create(
                slug=slug, name=name, emoji=emoji,
                description=desc, rule_type=rule, threshold=threshold,
            )

        categories = {name: Category.objects.create(name=name) for name in CATEGORIES}
        moods = {
            slug: Mood.objects.create(slug=slug, name=name, emoji=emoji)
            for slug, name, emoji in MOODS
        }

        for item in CAFES:
            cafe = Cafe.objects.create(
                name=item['name'],
                address=item['address'],
                description=item['description'],
                image=item['image'],
                category=categories[item['category']],
                opens_at=item['opens_at'],
                closes_at=item['closes_at'],
            )
            cafe.moods.set([moods[s] for s in item.get('moods', [])])
            for menu_name, price in item['menu']:
                MenuItem.objects.create(cafe=cafe, name=menu_name, price=price)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {len(CATEGORIES)} categories, {len(MOODS)} moods, '
            f'{len(BADGES)} badges, {len(CAFES)} cafes.'
        ))
