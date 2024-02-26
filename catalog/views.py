from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from catalog.models import Product, Contact, Blog
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView
from pytils.translit import slugify
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


class HomeListView(ListView):
    """Контроллер домашней страницы"""
    model = Product

    template_name = 'catalog/home_page.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.all()
        queryset = list(reversed(queryset))

        return queryset


class ContactTemplateView(TemplateView):
    """Контроллер страницы контактов"""
    contacts_list = Contact.objects.all()
    extra_context = {
        'contact_list': contacts_list,
    }
    template_name = 'catalog/contact.html'

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')
            print(f'You have a message from {name}({email}): {message}')
        return render(request, 'catalog/contact.html', context=self.extra_context)


class ProductListView(ListView):
    """Контроллер страницы товаров"""
    model = Product
    paginate_by = 6


class ProductCreateView(CreateView):
    """Контроллер страницы добавления товара от пользователя"""
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('catalog:products')


class ProductDetailView(DetailView):
    """Контроллер страницы товара по id"""
    model = Product


class ArticleListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        if self.object.views_count == 12:
            send_mail(
                'Test Subject',
                'Test message body',
                EMAIL_HOST_USER,
                ['dezhiter@mail.ru'],
                fail_silently=False,
            )
        self.object.save()
        return self.object


class ArticleCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published')
    success_url = reverse_lazy('catalog:articles')

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'image', 'is_published',)

    def form_valid(self, form):
        if form.is_valid():
            new_article = form.save()
            new_article.slug = slugify(new_article.title)
            new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.object.slug])


class ArticleDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:articles')
