# Домашняя работа 26 — формы

`Skystore` продолжает проект предыдущих домашних работ. Для товаров реализован полный CRUD через `ModelForm`, пользовательская валидация и безопасная загрузка изображений.

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
- общий базовый шаблон и подключаемый подшаблон меню `includes/menu.html`;
- полный CRUD товаров через `ProductForm` и Class-Based Views;
- единый список запрещённых слов для названия и описания товара с проверкой без учёта регистра;
- проверка, запрещающая отрицательную цену;
- стилизация всех полей формы через метод `__init__`;
- загрузка только JPEG/PNG размером не более 5 МБ;
- постраничный вывод каталога по четыре товара;
- все контроллеры приложения `catalog` переведены с FBV на CBV;
- отдельное приложение `blog`, зарегистрированное в `INSTALLED_APPS`;
- модель `BlogPost` с заголовком, содержимым, превью, датой, статусом публикации и просмотрами;
- полный CRUD статей на CBV по адресам `/blogs/.../`;
- в списке отображаются только опубликованные статьи;
- при открытии статьи атомарно увеличивается счётчик просмотров;
- после редактирования открывается изменённая статья;
- при достижении 100 просмотров отправляется поздравительное письмо;
- тесты моделей, CBV, CRUD, форм, страниц, пагинации и email-уведомления.

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
poetry run python lesson_22/manage.py loaddata blog_data
poetry run python lesson_22/manage.py createsuperuser
poetry run python lesson_22/manage.py runserver
```

Откройте `http://127.0.0.1:8000/`. Блог доступен по адресу `/blogs/`. Товар можно просмотреть по адресу `/products/<pk>/`, создать через `/products/create/`, изменить через `/products/<pk>/edit/` и удалить через `/products/<pk>/delete/`. Контакты доступны по адресу `/contacts/`, административная панель — `/admin/`.

Email отправителя и получателя уведомления о 100 просмотрах настраиваются переменными `DEFAULT_FROM_EMAIL` и `BLOG_NOTIFICATION_EMAIL` в `.env`.

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
poetry run python lesson_22/manage.py test catalog blog
```
