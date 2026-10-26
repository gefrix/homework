from decimal import Decimal
from tempfile import TemporaryDirectory

from catalog.admin import CategoryAdmin, ProductAdmin
from catalog.forms import ProductForm
from catalog.models import Category, Contact, Product
from catalog.views import ContactView, ProductCreateView, ProductDetailView, ProductListView
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse


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
        self.assertTemplateUsed(response, 'catalog/includes/menu.html')
        self.assertContains(response, 'Skystore')
        self.assertEqual(len(response.context['products']), 4)
        self.assertContains(response, 'page=2')

    def test_home_page_truncates_description_and_links_to_product(self) -> None:
        product = Product.objects.first()
        assert product is not None
        product.description = 'X' * 130
        product.save()

        response = self.client.get(reverse('catalog:home'))

        self.assertContains(response, 'X' * 90)
        self.assertNotContains(response, 'X' * 130)
        self.assertContains(response, reverse('catalog:product_detail', kwargs={'pk': product.pk}))

    def test_second_catalog_page_is_available(self) -> None:
        response = self.client.get(reverse('catalog:home'), {'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)

    def test_product_detail_displays_all_product_data(self) -> None:
        product = Product.objects.first()
        assert product is not None

        response = self.client.get(reverse('catalog:product_detail', kwargs={'pk': product.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertContains(response, product.name)
        self.assertContains(response, product.description)
        self.assertContains(response, product.category.name)
        self.assertContains(response, reverse('catalog:home'))

    def test_product_detail_returns_404_for_unknown_product(self) -> None:
        response = self.client.get(reverse('catalog:product_detail', kwargs={'pk': 999999}))

        self.assertEqual(response.status_code, 404)

    def test_product_create_form_requires_every_field(self) -> None:
        response = self.client.get(reverse('catalog:product_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_form.html')
        self.assertTrue(all(field.required for field in response.context['form'].fields.values()))

    def test_invalid_product_is_not_saved(self) -> None:
        products_before = Product.objects.count()

        response = self.client.post(
            reverse('catalog:product_create'),
            {'name': '', 'description': '', 'category': '', 'price': '-10'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Product.objects.count(), products_before)

    def test_valid_product_is_saved_and_redirected_to_detail(self) -> None:
        category = Category.objects.first()
        assert category is not None
        image = SimpleUploadedFile(
            'product.gif',
            (
                b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff'
                b'!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00'
                b'\x00\x02\x02D\x01\x00;'
            ),
            content_type='image/gif',
        )

        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse('catalog:product_create'),
                {
                    'name': 'Новый товар',
                    'description': 'Полное описание нового товара',
                    'category': category.pk,
                    'price': '249.90',
                    'image': image,
                },
            )

        product = Product.objects.get(name='Новый товар')
        self.assertRedirects(response, reverse('catalog:product_detail', kwargs={'pk': product.pk}))

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


class ProductFormTests(TestCase):
    def test_price_must_be_positive(self) -> None:
        category = Category.objects.create(name='Формы')
        form = ProductForm(
            data={
                'name': 'Товар',
                'description': 'Описание',
                'category': category.pk,
                'price': '0',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)


class CatalogAdminTests(SimpleTestCase):
    def test_category_list_columns(self) -> None:
        model_admin = CategoryAdmin(Category, admin.site)

        self.assertEqual(model_admin.list_display, ('id', 'name'))

    def test_product_list_filter_and_search(self) -> None:
        model_admin = ProductAdmin(Product, admin.site)

        self.assertEqual(model_admin.list_display, ('id', 'name', 'price', 'category'))
        self.assertEqual(model_admin.list_filter, ('category',))
        self.assertEqual(model_admin.search_fields, ('name', 'description'))


class CatalogCBVTests(SimpleTestCase):
    def test_all_catalog_routes_use_cbv(self) -> None:
        routes = (
            ('catalog:home', {}, ProductListView),
            ('catalog:product_create', {}, ProductCreateView),
            ('catalog:product_detail', {'pk': 1}, ProductDetailView),
            ('catalog:contacts', {}, ContactView),
        )

        for route_name, kwargs, view_class in routes:
            url = reverse(route_name, kwargs=kwargs)
            self.assertTrue(url.endswith('/'))
            self.assertIs(resolve(url).func.view_class, view_class)
