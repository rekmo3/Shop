from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="Назва")
    slug = models.SlugField(unique=True, verbose_name="Слаг для URL")

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:product_list_by_category", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Слаг для URL")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категорія"
    )
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Зображення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_active = models.BooleanField(default=True, verbose_name="У наявності")
    views = models.IntegerField(default=0, verbose_name="Кількість переглядів")

    def __str__(self):
        return f"{self.name} ({self.created_at:%d.%m.%Y})"

    def get_absolute_url(self):
        return reverse("main:product_detail", args=[self.id, self.slug])