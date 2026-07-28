from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('search/', views.search_products, name='search'),

    # Главная и категории
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='category_detail'),

    # Товары
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    #создание продукта
    path('create/', views.product_create, name='product_create'),

    # Поиск
    path('search/', views.search_products, name='search'),

    # Избранное (обычный редирект)
    path('toggle-favorite/<slug:product_slug>/', views.toggle_favorite, name='toggle_favorite'),

    # ============================================================
    # 🚀 AJAX-МАРШРУТЫ ДЛЯ ИЗБРАННОГО
    # ============================================================
    path('api/favorite/<slug:product_slug>/', views.api_toggle_favorite, name='api_toggle_favorite'),
    path('api/favorites-count/', views.api_favorites_count, name='api_favorites_count'),

    # Страница избранного
    path('favorites/', views.favorite_list, name='favorite_list'),

    path('delete/<slug:product_slug>/', views.product_delete, name='product_delete'),
]