from catalog.forms import ProductForm
from catalog.models import Contact, Product
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


def home(request: HttpRequest) -> HttpResponse:
    """Отобразить главную страницу интернет-магазина."""
    products = Product.objects.all()
    print('Последние пять товаров:', list(products[:5]))
    page_obj = Paginator(products, 4).get_page(request.GET.get('page'))
    return render(request, 'catalog/home.html', {'products': page_obj, 'page_obj': page_obj})


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Показать подробную информацию о выбранном товаре."""
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def product_create(request: HttpRequest) -> HttpResponse:
    """Создать товар из данных валидной формы."""
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save()
        return redirect('catalog:product_detail', pk=product.pk)

    return render(request, 'catalog/product_form.html', {'form': form})


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
