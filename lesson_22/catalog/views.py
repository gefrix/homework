from catalog.forms import ProductForm
from catalog.models import Contact, Product
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView


class ProductListView(ListView):
    """Отобразить каталог товаров с постраничной навигацией."""

    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'
    paginate_by = 4

    def get_queryset(self):
        products = Product.objects.all()
        print('Последние пять товаров:', list(products[:5]))
        return products


class ProductDetailView(DetailView):
    """Показать подробную информацию о выбранном товаре."""

    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    queryset = Product.objects.select_related('category')


class ProductCreateView(CreateView):
    """Создать товар из данных валидной формы."""

    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self) -> str:
        return reverse('catalog:product_detail', kwargs={'pk': self.object.pk})


class ContactView(View):
    """Отобразить контакты и обработать форму обратной связи."""

    template_name = 'catalog/contacts.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(
            request,
            self.template_name,
            {'contact': Contact.objects.filter(is_active=True).first(), 'success_message': ''},
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        form_data = {
            'name': request.POST.get('name', '').strip(),
            'phone': request.POST.get('phone', '').strip(),
            'message': request.POST.get('message', '').strip(),
        }
        print(f'Получены данные формы: {form_data}')
        return render(
            request,
            self.template_name,
            {
                'contact': Contact.objects.filter(is_active=True).first(),
                'success_message': 'Спасибо! Ваше сообщение успешно отправлено.',
            },
        )
