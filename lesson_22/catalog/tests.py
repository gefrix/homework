from decimal import Decimal
from io import BytesIO
from tempfile import TemporaryDirectory

from catalog.admin import CategoryAdmin, ProductAdmin
from catalog.forms import MAX_IMAGE_SIZE, ProductForm
from catalog.models import Category, Contact, Product
from catalog.views import (
    ContactView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
)
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import resolve, reverse
from PIL import Image


def create_uploaded_image(
    name: str = 'product.png', image_format: str = 'PNG', extra_bytes: int = 0
) -> SimpleUploadedFile:
    """Создать настоящее тестовое изображение без файлов в репозитории."""
    buffer = BytesIO()
    Image.new('RGB', (2, 2), color='blue').save(buffer, format=image_format)
    content_type = f'image/{"jpeg" if image_format == "JPEG" else image_format.lower()}'
    return SimpleUploadedFile(name, buffer.getvalue() + b'0' * extra_bytes, content_type=content_type)


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
        image = create_uploaded_image()

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

    def test_product_can_be_updated(self) -> None:
        product = Product.objects.first()
        category = Category.objects.first()
        assert product is not None
        assert category is not None

        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            response = self.client.post(
                reverse('catalog:product_update', kwargs={'pk': product.pk}),
                {
                    'name': 'Обновлённый товар',
                    'description': 'Новое описание',
                    'category': category.pk,
                    'price': '349.90',
                    'image': create_uploaded_image(),
                },
            )

        product.refresh_from_db()
        self.assertEqual(product.name, 'Обновлённый товар')
        self.assertRedirects(response, reverse('catalog:product_detail', kwargs={'pk': product.pk}))

    def test_product_can_be_deleted(self) -> None:
        product = Product.objects.first()
        assert product is not None

        response = self.client.post(reverse('catalog:product_delete', kwargs={'pk': product.pk}))

        self.assertRedirects(response, reverse('catalog:home'))
        self.assertFalse(Product.objects.filter(pk=product.pk).exists())

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
    @classmethod
    def setUpTestData(cls) -> None:
        cls.category = Category.objects.create(name='Формы')

    def form_data(self, **overrides: str) -> dict[str, str | int]:
        data: dict[str, str | int] = {
            'name': 'Полезный товар',
            'description': 'Подробное описание продукта',
            'category': self.category.pk,
            'price': '100.00',
        }
        data.update(overrides)
        return data

    def test_forbidden_words_are_rejected_in_name_and_description_case_insensitively(self) -> None:
        cases = (
            {'name': 'БЕСПЛАТНО для всех'},
            {'description': 'Новая КрипТоВалюта для клиентов'},
        )

        for values in cases:
            with self.subTest(values=values):
                form = ProductForm(data=self.form_data(**values), files={'image': create_uploaded_image()})

                self.assertFalse(form.is_valid())
                field_name = next(iter(values))
                self.assertIn(field_name, form.errors)
                self.assertIn('запрещённые слова', form.errors[field_name][0])

    def test_price_must_not_be_negative(self) -> None:
        form = ProductForm(
            data=self.form_data(price='-0.01'),
            files={'image': create_uploaded_image()},
        )

        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        self.assertIn('не может быть отрицательной', form.errors['price'][0])

    def test_zero_price_is_allowed(self) -> None:
        form = ProductForm(
            data=self.form_data(price='0'),
            files={'image': create_uploaded_image()},
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_all_form_fields_receive_bootstrap_styles_in_init(self) -> None:
        form = ProductForm()

        for field in form.fields.values():
            expected_class = 'form-select' if field is form.fields['category'] else 'form-control'
            self.assertEqual(field.widget.attrs['class'], expected_class)

    def test_jpeg_and_png_images_are_allowed(self) -> None:
        for name, image_format in (('product.jpg', 'JPEG'), ('product.png', 'PNG')):
            with self.subTest(image_format=image_format):
                form = ProductForm(
                    data=self.form_data(),
                    files={'image': create_uploaded_image(name, image_format)},
                )

                self.assertTrue(form.is_valid(), form.errors)

    def test_gif_image_is_rejected(self) -> None:
        form = ProductForm(
            data=self.form_data(),
            files={'image': create_uploaded_image('product.gif', 'GIF')},
        )

        self.assertFalse(form.is_valid())
        self.assertIn('JPEG и PNG', form.errors['image'][0])

    def test_image_larger_than_five_megabytes_is_rejected(self) -> None:
        form = ProductForm(
            data=self.form_data(),
            files={'image': create_uploaded_image(extra_bytes=MAX_IMAGE_SIZE)},
        )

        self.assertFalse(form.is_valid())
        self.assertIn('5 МБ', form.errors['image'][0])


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
            ('catalog:product_update', {'pk': 1}, ProductUpdateView),
            ('catalog:product_delete', {'pk': 1}, ProductDeleteView),
            ('catalog:contacts', {}, ContactView),
        )

        for route_name, kwargs, view_class in routes:
            url = reverse(route_name, kwargs=kwargs)
            self.assertTrue(url.endswith('/'))
            self.assertIs(resolve(url).func.view_class, view_class)
