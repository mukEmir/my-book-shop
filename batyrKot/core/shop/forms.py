from django import forms
from .models import Product, Category

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'discount', 'stock', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'help_text': 'Оставьте пустым для автоматической генерации из названия'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'category': 'Категория',
            'name': 'Название книги',
            'slug': 'URL-идентификатор (можно оставить пустым)',
            'description': 'Описание',
            'price': 'Цена (₽)',
            'discount': 'Скидка (%)',
            'stock': 'Количество на складе',
            'image': 'Обложка книги',
        }

    # Делаем slug необязательным (если пользователь не заполнил — сгенерируется автоматически)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False