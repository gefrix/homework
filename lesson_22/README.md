# Домашняя работа 23 — работа с ORM в Django

`Skystore` продолжает проект предыдущей домашней работы. Каталог теперь хранится в PostgreSQL и управляется через Django ORM и административную панель.

## Реализовано

- модели `Category`, `Product` и дополнительная модель `Contact`;
- связь товара с категорией через `ForeignKey`;
- изображения товаров через `ImageField` и настройки `MEDIA_URL`/`MEDIA_ROOT`;
- PostgreSQL с параметрами подключения из `.env`;
- административная панель со списками, фильтром и поиском;
- фикстура категорий, товаров и контактных данных;
- команда `load_catalog_data`, которая очищает каталог и заново загружает фикстуру;
- вывод пяти последних товаров на главной странице и в консоль сервера;
- вывод активных контактных данных из базы на странице `/contacts/`;
- тесты моделей, страниц и пользовательской команды.

## Настройка PostgreSQL

Создайте базу и пользователя PostgreSQL:

```sql
CREATE USER skystore WITH PASSWORD 'your_password';
CREATE DATABASE skystore OWNER skystore;
```

Скопируйте шаблон настроек и укажите свой пароль:

```powershell
Copy-Item lesson_22/.env.example lesson_22/.env
```

Файл `.env` не добавляется в Git. В репозитории хранится только безопасный шаблон `.env.example`.

## Запуск

Из корня репозитория:

```powershell
poetry install
poetry run python lesson_22/manage.py migrate
poetry run python lesson_22/manage.py load_catalog_data
poetry run python lesson_22/manage.py createsuperuser
poetry run python lesson_22/manage.py runserver
```

Откройте `http://127.0.0.1:8000/`, контакты — `/contacts/`, административную панель — `/admin/`.

## Фикстура и shell

Обычная загрузка фикстуры:

```powershell
poetry run python lesson_22/manage.py loaddata catalog_data
```

Команда с предварительной очисткой товаров и категорий:

```powershell
poetry run python lesson_22/manage.py load_catalog_data
```

Интерактивная оболочка IPython:

```powershell
poetry run python lesson_22/manage.py shell
```

Скриншоты операций ORM сохранены в каталоге `screenshots`.

## Проверка

```powershell
poetry run python lesson_22/manage.py check
poetry run python lesson_22/manage.py makemigrations --check
poetry run python lesson_22/manage.py test catalog
```
