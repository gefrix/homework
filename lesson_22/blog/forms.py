"""Формы приложения blog."""

from blog.models import BlogPost
from django import forms


class BlogPostForm(forms.ModelForm):
    """Форма создания и редактирования статьи."""

    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'preview', 'is_published')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
