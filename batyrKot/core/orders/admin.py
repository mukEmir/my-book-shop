from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'status', 'total_price']  # Поля, видимые в списке
    list_filter = ['status', 'created_at']                        # Фильтры справа
    inlines = [OrderItemInline]                                   # Чтобы товары отображались прямо внутри заказа