from .models import Category

def categories_nav(request):
    return {
        'categories': Category.objects.all()
    }