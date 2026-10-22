"""Очистить каталог и загрузить тестовые данные из фикстуры."""

from typing import Any

from catalog.models import Category, Product
from django.core.management import BaseCommand, call_command
from django.db import transaction


class Command(BaseCommand):
    help = 'Удаляет товары и категории, затем загружает catalog_data.json'

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'catalog_data', verbosity=options['verbosity'])
        self.stdout.write(self.style.SUCCESS('Тестовые данные каталога успешно загружены.'))
