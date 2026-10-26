# Домашняя работа 25 «FBV и CBV»

## Изменения

- все контроллеры приложения `catalog`, включая контакты, переведены на CBV;
- создано и зарегистрировано приложение `blog` с отдельным `urls.py`;
- добавлена модель `BlogPost`, миграция, административная панель и тестовая фикстура;
- полный CRUD статей реализован через `ListView`, `DetailView`, `CreateView`, `UpdateView` и `DeleteView`;
- все маршруты блога находятся под `/blogs/` и заканчиваются `/`;
- блоговые шаблоны наследуют `catalog/base.html` и используют общий `includes/menu.html`;
- список фильтруется по `is_published=True`;
- `DetailView.get_object()` атомарно увеличивает счётчик просмотров;
- `UpdateView.success_url` возвращает пользователя к отредактированной статье;
- при достижении 100 просмотров отправляется email-поздравление;
- добавлены тесты CBV, модели, полного CRUD, фильтрации, просмотров и email.

## Проверка

- `poetry install`;
- `python manage.py check`;
- `python manage.py makemigrations --check`;
- `python manage.py test catalog blog`;
- `python manage.py loaddata blog_data`;
- `black --check lesson_22`;
- `isort --check-only lesson_22`;
- `flake8 lesson_22`;
- ручная проверка каталога и всех страниц блога.
