from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Mood(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=8, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Cafe(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='cafes',
    )
    moods = models.ManyToManyField(Mood, related_name='cafes', blank=True)
    opens_at = models.TimeField(default='09:00')
    closes_at = models.TimeField(default='22:00')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='menu_items',
    )
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.cafe.name})'


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField()
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'cafe'], name='unique_user_cafe_review'),
        ]

    def __str__(self):
        return f'{self.user} → {self.cafe} ({self.rating})'


class Badge(models.Model):
    RULE_CHOICES = (
        ('reservations', 'Reservations count'),
        ('reviews', 'Reviews count'),
        ('categories', 'Distinct categories visited'),
        ('favorites', 'Favorites count'),
    )

    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    emoji = models.CharField(max_length=8, blank=True)
    description = models.CharField(max_length=200, blank=True)
    rule_type = models.CharField(max_length=20, choices=RULE_CHOICES)
    threshold = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['threshold', 'name']

    def __str__(self):
        return self.name


class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    cafe = models.ForeignKey(
        Cafe,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f'{self.user} @ {self.cafe} on {self.date} {self.time}'
