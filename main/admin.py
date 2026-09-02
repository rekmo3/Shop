from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'price', 'is_active', 'created_at', 'image_tag')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return format_html('<span>немає зображення</span>')

    image_tag.short_description = "Зображення"