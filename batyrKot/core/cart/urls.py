from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Корзина — просмотр
    path('', views.cart_detail, name='detail'),

    # Добавление товара в корзину
    path('add/<slug:product_slug>/', views.cart_add, name='add'),

    # Удаление позиции из корзины
    path('remove/<int:item_id>/', views.cart_remove, name='remove'),

    # Обновление количества товара
    path('update/<int:item_id>/', views.cart_update, name='update'),

    # ============================================================
    # 🚀 AJAX-маршруты (без перезагрузки страницы)
    # ============================================================

    # AJAX: добавить товар
    path('api/add/<slug:product_slug>/', views.api_cart_add, name='api_add'),

    # AJAX: удалить товар
    path('api/remove/<int:item_id>/', views.api_cart_remove, name='api_remove'),

    # AJAX: обновить количество
    path('api/update/<int:item_id>/', views.api_cart_update, name='api_update'),

    # AJAX: получить количество товаров в корзине
    path('api/count/', views.api_cart_count, name='api_count'),
]