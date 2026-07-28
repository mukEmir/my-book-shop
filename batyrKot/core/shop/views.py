from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.text import slugify
import uuid

from .models import Category, Product, Favorite
from .forms import ProductCreateForm
from cart.models import Cart, CartItem


class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)

        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        in_stock = self.request.GET.get('in_stock')
        if in_stock == 'on':
            queryset = queryset.filter(stock__gt=0)

        categories = self.request.GET.getlist('categories')
        if categories:
            queryset = queryset.filter(category__slug__in=categories)

        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_filters'] = self.request.GET.copy()
        context['all_categories'] = Category.objects.all()
        if 'category_slug' in self.kwargs:
            context['current_category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorite.objects.filter(
                user=self.request.user,
                product=self.object
            ).exists()
        return context


@login_required
def toggle_favorite(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return redirect('shop:product_detail', slug=product_slug)


def search_products(request):
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    in_stock = request.GET.get('in_stock')

    products = Product.objects.filter(available=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if in_stock:
        products = products.filter(stock__gt=0)

    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.all(),
        'selected_category': category_slug,
    }
    return render(request, 'shop/search_results.html', context)


# ============================================================
# 🚀 AJAX-МЕТОДЫ ДЛЯ ИЗБРАННОГО
# ============================================================

@login_required
def api_toggle_favorite(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    favorite, created = Favorite.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        favorite.delete()
        is_favorite = False
        message = f'{product.name} удалён из избранного'
    else:
        is_favorite = True
        message = f'{product.name} добавлен в избранное'

    total_favorites = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({
        'success': True,
        'is_favorite': is_favorite,
        'total_favorites': total_favorites,
        'message': message
    })


@login_required
def api_favorites_count(request):
    total_favorites = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({
        'total_favorites': total_favorites
    })


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'shop/favorite_list.html', {'favorites': favorites})


# ============================================================
# 🚀 СОЗДАНИЕ КНИГИ (ДЛЯ АВТОРИЗОВАННЫХ ПОЛЬЗОВАТЕЛЕЙ)
# ============================================================

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.available = True
            product.created_by = request.user

            # Если slug пустой — генерируем из названия
            if not product.slug:
                product.slug = slugify(product.name)
                if Product.objects.filter(slug=product.slug).exists():
                    product.slug = f"{product.slug}-{uuid.uuid4().hex[:4]}"

            product.save()
            messages.success(request, f'Книга "{product.name}" успешно добавлена!')
            return redirect('shop:product_detail', slug=product.slug)
    else:
        form = ProductCreateForm()
    return render(request, 'shop/product_create.html', {'form': form})


@login_required
def product_delete(request, product_slug):
    """Удаление книги (только для автора)"""
    product = get_object_or_404(Product, slug=product_slug)

    # Проверяем, что текущий пользователь — автор книги
    if product.created_by != request.user:
        messages.error(request, 'Вы не можете удалить эту книгу.')
        return redirect('shop:product_list')

    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Книга "{product_name}" удалена!')
        return redirect('users:profile')

    return render(request, 'shop/product_confirm_delete.html', {'product': product})


from django.db.models import Q
from .models import Product


def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            available=True
        )

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'shop/search_results.html', context)