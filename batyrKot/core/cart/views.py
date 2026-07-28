from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from shop.models import Product
from .models import Cart, CartItem
import json


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
@login_required
def cart_add(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += int(request.POST.get('quantity', 1))
    else:
        cart_item.quantity = int(request.POST.get('quantity', 1))
    cart_item.save()
    return redirect('cart:detail')


@require_POST
@login_required
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:detail')


@require_POST
@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart:detail')


# ============================================================
# 🚀 НОВЫЕ AJAX-МЕТОДЫ (без перезагрузки страницы)
# ============================================================

@require_POST
@login_required
def api_cart_add(request, product_slug):
    """AJAX: добавить товар в корзину"""
    product = get_object_or_404(Product, slug=product_slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    quantity = int(request.POST.get('quantity', 1))
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return JsonResponse({
        'success': True,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price),
        'item_quantity': cart_item.quantity,
        'item_total': str(cart_item.total_price),
        'message': f'{product.name} добавлен в корзину'
    })


@require_POST
@login_required
def api_cart_remove(request, item_id):
    """AJAX: удалить товар из корзины"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()

    cart = Cart.objects.get(user=request.user)
    return JsonResponse({
        'success': True,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price),
        'message': f'{product_name} удалён из корзины'
    })


@require_POST
@login_required
def api_cart_update(request, item_id):
    """AJAX: обновить количество товара"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    data = json.loads(request.body)
    quantity = int(data.get('quantity', 1))

    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()

    cart = Cart.objects.get(user=request.user)
    return JsonResponse({
        'success': True,
        'total_items': cart.total_items,
        'total_price': str(cart.total_price),
        'item_total': str(cart_item.total_price if quantity > 0 else 0),
        'quantity': quantity if quantity > 0 else 0,
        'message': 'Количество обновлено' if quantity > 0 else 'Товар удалён'
    })


@login_required
def api_cart_count(request):
    """AJAX: получить количество товаров в корзине"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return JsonResponse({
        'total_items': cart.total_items,
        'total_price': str(cart.total_price)
    })