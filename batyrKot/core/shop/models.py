from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
import os
from django.utils.text import slugify
import uuid

User = get_user_model()


def product_image_path(instance, filename):
    """Генерирует имя для загружаемого файла: убирает пробелы, переводит в латиницу, добавляет уникальный хеш"""
    ext = filename.split('.')[-1] if '.' in filename else ''
    name = slugify(instance.name)[:50]
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{name}_{unique_id}.{ext}" if ext else f"{name}_{unique_id}"
    return os.path.join('products/', filename)


def category_image_path(instance, filename):
    """То же самое для категорий"""
    ext = filename.split('.')[-1] if '.' in filename else ''
    name = slugify(instance.name)[:30]
    unique_id = uuid.uuid4().hex[:8]
    filename = f"{name}_{unique_id}.{ext}" if ext else f"{name}_{unique_id}"
    return os.path.join('categories/', filename)


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ImageField(upload_to=category_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # <-- разрешаем пустой для авто-генерации
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text='Скидка в %')
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_products')  # <-- добавлено
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    @property
    def final_price(self):
        if self.discount > 0:
            return self.price * (1 - Decimal(self.discount) / Decimal(100))
        return self.price

    # ============================================================
    # 🚀 АВТОМАТИЧЕСКАЯ ГЕНЕРАЦИЯ SLUG ПРИ СОХРАНЕНИИ
    # ============================================================
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Если slug уже занят — добавляем ID или случайное число
            if Product.objects.filter(slug=self.slug).exclude(id=self.id).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:4]}"
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')