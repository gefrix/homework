"""Формы приложения catalog."""

from decimal import Decimal
from typing import Any

from catalog.models import Product
from django import forms
from django.core.files.uploadedfile import UploadedFile

FORBIDDEN_WORDS = (
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
)
ALLOWED_IMAGE_FORMATS = {'JPEG', 'PNG'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


class ProductForm(forms.ModelForm):
    """Форма создания и редактирования товара с пользовательской валидацией."""

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'category', 'price')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/jpeg,image/png'}),
            'price': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            css_class = 'form-check-input' if isinstance(field.widget, forms.CheckboxInput) else 'form-control'
            if isinstance(field.widget, forms.Select):
                css_class = 'form-select'
            field.widget.attrs['class'] = css_class

    @staticmethod
    def _validate_forbidden_words(value: str) -> str:
        """Проверить текст на запрещённые слова без учёта регистра."""
        normalized_value = value.casefold()
        found_words = [word for word in FORBIDDEN_WORDS if word.casefold() in normalized_value]
        if found_words:
            raise forms.ValidationError(
                'Нельзя использовать запрещённые слова: %(words)s.',
                params={'words': ', '.join(found_words)},
            )
        return value

    def clean_name(self) -> str:
        """Не допустить запрещённые слова в названии."""
        return self._validate_forbidden_words(self.cleaned_data['name'])

    def clean_description(self) -> str:
        """Не допустить запрещённые слова в описании."""
        return self._validate_forbidden_words(self.cleaned_data['description'])

    def clean_price(self) -> Decimal:
        """Не допустить сохранение отрицательной цены."""
        price: Decimal = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price

    def clean_image(self) -> Any:
        """Разрешить новые изображения JPEG/PNG размером не более 5 МБ."""
        image = self.cleaned_data['image']
        if not isinstance(image, UploadedFile):
            return image

        if image.size > MAX_IMAGE_SIZE:
            raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')

        image_format = getattr(getattr(image, 'image', None), 'format', '').upper()
        if image_format not in ALLOWED_IMAGE_FORMATS:
            raise forms.ValidationError('Допустимы только изображения JPEG и PNG.')
        return image
