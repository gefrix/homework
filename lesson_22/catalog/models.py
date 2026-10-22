"""Модели каталога интернет-магазина."""

from django.db import models


class Category(models.Model):
    """Категория товаров."""

    name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Товар, доступный в каталоге."""

    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(blank=True, verbose_name='описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='изображение')
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name='категория',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена за покупку')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.name


class Contact(models.Model):
    """Контактные данные компании для страницы обратной связи."""

    country = models.CharField(max_length=100, verbose_name='страна')
    tax_id = models.CharField(max_length=30, verbose_name='ИНН')
    address = models.CharField(max_length=255, verbose_name='адрес')
    phone = models.CharField(max_length=30, blank=True, verbose_name='телефон')
    email = models.EmailField(blank=True, verbose_name='электронная почта')
    is_active = models.BooleanField(default=True, verbose_name='отображать на сайте')

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'

    def __str__(self) -> str:
        return f'{self.country}: {self.address}'
