from decimal import Decimal

from catalog.admin import CategoryAdmin, ProductAdmin
from catalog.models import Category, Contact, Product
from django.contrib import admin
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class CatalogViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        category = Category.objects.create(name='Тестовая категория')
        for number in range(6):
            Product.objects.create(
                name=f'Товар {number}',
                description='Описание товара',
                category=category,
                price=Decimal('100.00') + number,
            )
        Contact.objects.create(
            country='Россия',
            tax_id='1234567890',
            address='Москва',
            phone='+7 900 000-00-00',
            email='test@example.com',
        )

    def test_home_page_is_available(self) -> None:
        response = self.client.get(reverse('catalog:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')
        self.assertContains(response, 'Skystore')
        self.assertEqual(len(response.context['products']), 5)

    def test_contacts_page_is_available(self) -> None:
        response = self.client.get(reverse('catalog:contacts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/contacts.html')
        self.assertContains(response, 'Контакты')
        self.assertContains(response, 'test@example.com')

    def test_contacts_form_displays_success_message(self) -> None:
        response = self.client.post(
            reverse('catalog:contacts'),
            {
                'name': 'Анна',
                'phone': '+7 900 000-00-00',
                'message': 'Хочу узнать подробнее о продукте.',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ваше сообщение успешно отправлено')


class CatalogModelsTests(TestCase):
    def test_model_string_representations(self) -> None:
        category = Category.objects.create(name='Интеграции')
        product = Product.objects.create(
            name='API Starter',
            category=category,
            price=Decimal('150.00'),
        )

        self.assertEqual(str(category), 'Интеграции')
        self.assertEqual(str(product), 'API Starter')
        self.assertEqual(Product._meta.verbose_name_plural, 'товары')

    def test_load_catalog_data_command_replaces_catalog(self) -> None:
        category = Category.objects.create(name='Будет удалена')
        Product.objects.create(name='Будет удалён', category=category, price=Decimal('1.00'))

        call_command('load_catalog_data', verbosity=0)

        self.assertFalse(Category.objects.filter(name='Будет удалена').exists())
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Product.objects.count(), 5)
        self.assertTrue(Product.objects.filter(category__name='Веб-разработка').exists())


class CatalogAdminTests(SimpleTestCase):
    def test_category_list_columns(self) -> None:
        model_admin = CategoryAdmin(Category, admin.site)

        self.assertEqual(model_admin.list_display, ('id', 'name'))

    def test_product_list_filter_and_search(self) -> None:
        model_admin = ProductAdmin(Product, admin.site)

        self.assertEqual(model_admin.list_display, ('id', 'name', 'price', 'category'))
        self.assertEqual(model_admin.list_filter, ('category',))
        self.assertEqual(model_admin.search_fields, ('name', 'description'))
