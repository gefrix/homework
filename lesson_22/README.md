# Домашняя работа 22 — знакомство с Django

`Skystore` — учебный интернет-магазин цифровых продуктов. Проект создан на Django и содержит приложение `catalog` с каталогом товаров и страницей контактов.

## Реализовано

- Django-проект `config`;
- приложение `catalog`, зарегистрированное в `INSTALLED_APPS`;
- URL-конфигурация приложения подключена через `include`;
- главная страница доступна по адресу `/`;
- страница контактов доступна по адресу `/contacts/`;
- обе страницы рендерятся функцией `render`;
- Bootstrap и статические CSS/JS-файлы;
- форма обратной связи с CSRF-защитой;
- вывод принятых данных в консоль и сообщение об успешной отправке;
- автоматические тесты контроллеров и формы.

## Запуск

Из корня репозитория:

```powershell
poetry install
poetry run python lesson_22/manage.py migrate
poetry run python lesson_22/manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Проверка

```powershell
poetry run python lesson_22/manage.py check
poetry run python lesson_22/manage.py test catalog
poetry run python lesson_22/manage.py findstatic catalog/css/styles.css
```
