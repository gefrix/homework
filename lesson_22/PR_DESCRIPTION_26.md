## Что сделано

- Реализован полный CRUD товаров на Class-Based Views: создание, просмотр, редактирование и удаление.
- Добавлены маршруты и шаблон подтверждения удаления товара.
- Форма создания и редактирования товара построена на `django.forms.ModelForm`.
- Список запрещённых слов вынесен в константу и применяется к названию и описанию без учёта регистра.
- В `clean_price` добавлена понятная ошибка для отрицательной цены.
- Все виджеты получают Bootstrap-классы в `ProductForm.__init__`; предусмотрен отдельный класс для чекбоксов.
- Загрузка изображений ограничена форматами JPEG/PNG и размером 5 МБ.
- Дополнены страницы товара, документация и автотесты.

## Проверка

```powershell
poetry run black --check lesson_22
poetry run isort --check-only lesson_22
poetry run flake8 lesson_22
poetry run pytest -q
poetry run python lesson_22/manage.py check
poetry run python lesson_22/manage.py makemigrations --check --dry-run
poetry run python lesson_22/manage.py test catalog blog
```
