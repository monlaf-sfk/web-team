from django.db import models

from apps.common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Cafe(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='cafes'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='cafes/', blank=True)
    is_popular = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'cafes'

    def __str__(self):
        return self.name


class MenuItem(BaseModel):
    cafe = models.ForeignKey(
        Cafe, on_delete=models.CASCADE, related_name='menu_items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} — {self.price}'
