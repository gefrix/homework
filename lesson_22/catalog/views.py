from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

PRODUCTS = [
    {
        'name': 'Удобный сервис рассылок',
        'price': 140,
        'features': [
            'Неограниченная лицензия',
            'Поддержка',
            'Установка на сервер',
            'Получение обновлений',
        ],
    },
    {
        'name': 'Telegram-бот для бизнеса',
        'price': 120,
        'features': [
            'Готовый сценарий',
            'Настройка команд',
            'Подключение к API',
            'Техническая поддержка',
        ],
    },
    {
        'name': 'Набор полезных утилит',
        'price': 90,
        'features': [
            'Пять приложений',
            'Исходный код',
            'Документация',
            'Бесплатные обновления',
        ],
    },
    {
        'name': 'Шаблон веб-приложения',
        'price': 180,
        'features': [
            'Адаптивный интерфейс',
            'Панель управления',
            'Готовые страницы',
            'Помощь с запуском',
        ],
    },
]


def home(request: HttpRequest) -> HttpResponse:
    """Отобразить главную страницу интернет-магазина."""
    return render(request, 'catalog/home.html', {'products': PRODUCTS})


def contacts(request: HttpRequest) -> HttpResponse:
    """Отобразить контакты и обработать форму обратной связи."""
    success_message = ''

    if request.method == 'POST':
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'message': request.POST.get('message', '').strip(),
        }
        print(f'Получены данные формы: {form_data}')
        success_message = 'Спасибо! Ваше сообщение успешно отправлено.'

    return render(
        request,
        'catalog/contacts.html',
        {'success_message': success_message},
    )
