from blog.models import BlogPost
from blog.views import (
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)
from django.core import mail
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import resolve, reverse


class BlogPostModelTests(TestCase):
    def test_string_and_meta(self) -> None:
        post = BlogPost.objects.create(title='Django CBV', content='Содержимое')

        self.assertEqual(str(post), 'Django CBV')
        self.assertEqual(BlogPost._meta.verbose_name, 'статья')
        self.assertEqual(BlogPost._meta.verbose_name_plural, 'статьи')


class BlogPostViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.published = BlogPost.objects.create(
            title='Опубликованная статья',
            content='Полезный материал о Django.',
            is_published=True,
        )
        cls.draft = BlogPost.objects.create(
            title='Черновик',
            content='Эта статья ещё не готова.',
            is_published=False,
        )

    def test_list_contains_only_published_posts(self) -> None:
        response = self.client.get(reverse('blog:blog_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogpost_list.html')
        self.assertTemplateUsed(response, 'catalog/base.html')
        self.assertTemplateUsed(response, 'catalog/includes/menu.html')
        self.assertContains(response, self.published.title)
        self.assertNotContains(response, self.draft.title)

    def test_detail_increments_views_count(self) -> None:
        url = reverse('blog:blog_detail', kwargs={'pk': self.published.pk})

        self.client.get(url)
        self.client.get(url)

        self.published.refresh_from_db()
        self.assertEqual(self.published.views_count, 2)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        BLOG_NOTIFICATION_EMAIL='owner@example.com',
    )
    def test_email_is_sent_when_post_reaches_100_views(self) -> None:
        self.published.views_count = 99
        self.published.save(update_fields=('views_count',))

        self.client.get(reverse('blog:blog_detail', kwargs={'pk': self.published.pk}))

        self.published.refresh_from_db()
        self.assertEqual(self.published.views_count, 100)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('100 просмотров', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['owner@example.com'])

    def test_create_view_saves_post(self) -> None:
        response = self.client.post(
            reverse('blog:blog_create'),
            {
                'title': 'Новая статья',
                'content': 'Новый полезный материал.',
                'is_published': 'on',
            },
        )

        post = BlogPost.objects.get(title='Новая статья')
        self.assertRedirects(response, reverse('blog:blog_detail', kwargs={'pk': post.pk}))

    def test_update_redirects_to_edited_post(self) -> None:
        response = self.client.post(
            reverse('blog:blog_update', kwargs={'pk': self.published.pk}),
            {
                'title': 'Обновлённая статья',
                'content': self.published.content,
                'is_published': 'on',
            },
        )

        self.published.refresh_from_db()
        self.assertEqual(self.published.title, 'Обновлённая статья')
        self.assertRedirects(response, reverse('blog:blog_detail', kwargs={'pk': self.published.pk}))

    def test_delete_view_removes_post(self) -> None:
        response = self.client.post(reverse('blog:blog_delete', kwargs={'pk': self.draft.pk}))

        self.assertRedirects(response, reverse('blog:blog_list'))
        self.assertFalse(BlogPost.objects.filter(pk=self.draft.pk).exists())


class BlogPostRoutingTests(SimpleTestCase):
    def test_all_blog_routes_use_cbv_and_end_with_slash(self) -> None:
        routes = (
            ('blog:blog_list', {}, BlogPostListView),
            ('blog:blog_create', {}, BlogPostCreateView),
            ('blog:blog_detail', {'pk': 1}, BlogPostDetailView),
            ('blog:blog_update', {'pk': 1}, BlogPostUpdateView),
            ('blog:blog_delete', {'pk': 1}, BlogPostDeleteView),
        )

        for route_name, kwargs, view_class in routes:
            url = reverse(route_name, kwargs=kwargs)
            self.assertTrue(url.endswith('/'))
            self.assertIs(resolve(url).func.view_class, view_class)
