from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Оформление заказа (страница с формой и переход на Stripe)
    path('checkout/', views.checkout, name='checkout'),

    # Успешная оплата (колбэк от Stripe)
    path('success/', views.order_success, name='success'),

    # Отмена оплаты (перенаправляет в историю)
    path('cancel/', views.order_history, name='cancel'),

    # История заказов пользователя
    path('history/', views.order_history, name='history'),
]