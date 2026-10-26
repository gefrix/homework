from blog.forms import BlogPostForm
from blog.models import BlogPost
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F, QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class BlogPostListView(ListView):
    """Показать только опубликованные статьи."""

    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self) -> QuerySet[BlogPost]:
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    """Показать статью и увеличить счётчик просмотров."""

    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset: QuerySet[BlogPost] | None = None) -> BlogPost:
        post = super().get_object(queryset)
        BlogPost.objects.filter(pk=post.pk).update(views_count=F('views_count') + 1)
        post.refresh_from_db(fields=('views_count',))

        if post.views_count == 100:
            send_mail(
                subject=f'Статья «{post.title}» набрала 100 просмотров',
                message=f'Поздравляем! Статья «{post.title}» достигла отметки в 100 просмотров.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.BLOG_NOTIFICATION_EMAIL],
                fail_silently=False,
            )

        return post


class BlogPostCreateView(CreateView):
    """Создать новую статью."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'

    def get_success_url(self) -> str:
        return reverse('blog:blog_detail', kwargs={'pk': self.object.pk})


class BlogPostUpdateView(UpdateView):
    """Отредактировать статью и открыть её подробную страницу."""

    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blogpost_form.html'
    success_url = '/blogs/{id}/'


class BlogPostDeleteView(DeleteView):
    """Удалить статью после подтверждения."""

    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blog_list')
