from catalog.models import Contact, Product
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    """Отобразить главную страницу интернет-магазина."""
    products = Product.objects.select_related('category').order_by('-created_at')[:5]
    print('Последние пять товаров:', list(products))
    return render(request, 'catalog/home.html', {'products': products})


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
        {
            'contact': Contact.objects.filter(is_active=True).first(),
            'success_message': success_message,
        },
    )
