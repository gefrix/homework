"""Формы приложения catalog."""

from decimal import Decimal
from typing import Any

from catalog.models import Product
from django import forms


class ProductForm(forms.ModelForm):
    """Форма создания нового товара."""

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    def clean_price(self) -> Decimal:
        """Не допустить сохранение нулевой или отрицательной цены."""
        price: Decimal = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('Цена должна быть больше нуля.')
        return price
