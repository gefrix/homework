# Домашняя работа 24 — шаблонизация в Django

`Skystore` продолжает проект предыдущих домашних работ. Каталог хранится в PostgreSQL, а страницы формируются из общих и специализированных Django-шаблонов.

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
- страница с полной информацией о товаре по адресу `/products/<pk>/`;
- карточки товаров со ссылками на подробную страницу и описанием до 100 символов;
- общий базовый шаблон и подключаемый подшаблон навигации;
- форма создания товара с обязательными полями, проверкой цены и загрузкой изображения;
- постраничный вывод каталога по четыре товара;
- тесты моделей, форм, страниц, пагинации и пользовательской команды.

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

Откройте `http://127.0.0.1:8000/`. Страница товара доступна по адресу `/products/<pk>/`, форма добавления — `/products/create/`, контакты — `/contacts/`, административная панель — `/admin/`.

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
