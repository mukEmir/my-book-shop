import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.models import Cart
from .models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    if cart.total_items == 0:
        return redirect('cart:detail')

    if request.method == 'POST':
        # создаём заказ
        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            shipping_address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            comment=request.POST.get('comment', ''),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.final_price,
            )
        # очищаем корзину
        cart.items.all().delete()

        # создаём Stripe сессию
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Order #{order.id}'},
                    'unit_amount': int(order.total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('orders:success')) + f'?order_id={order.id}',
            cancel_url=request.build_absolute_uri(reverse('orders:cancel')),
        )
        order.stripe_payment_id = session.id
        order.save()
        return redirect(session.url, code=303)

    return render(request, 'orders/checkout.html', {'cart': cart})

@login_required
def order_success(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/history.html', {'orders': orders})