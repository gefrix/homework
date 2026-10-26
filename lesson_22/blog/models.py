from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    """Статья блога Skystore."""

    title = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name='превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='количество просмотров')

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('-created_at',)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse('blog:blog_detail', kwargs={'pk': self.pk})
