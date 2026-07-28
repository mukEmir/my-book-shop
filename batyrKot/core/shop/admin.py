from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'discount', 'category', 'available']
    list_filter = ['available', 'category']
    list_editable = ['price', 'stock', 'discount', 'available']
    prepopulated_fields = {'slug': ('name',)}