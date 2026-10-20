from django.test import TestCase
from django.urls import reverse


class CatalogViewsTests(TestCase):
    def test_home_page_is_available(self) -> None:
        response = self.client.get(reverse('catalog:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/home.html')
        self.assertContains(response, 'Skystore')

    def test_contacts_page_is_available(self) -> None:
        response = self.client.get(reverse('catalog:contacts'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/contacts.html')
        self.assertContains(response, 'Контакты')

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
