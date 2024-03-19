from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.forms import VersionForm, ProductForm
from catalog.models import Product, Contact, Version
from django.views.generic import ListView, CreateView, DetailView, TemplateView, UpdateView, DeleteView


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

    def get_queryset(self):
        return Product.objects.order_by('pk')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Контроллер страницы добавления товара от пользователя"""
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def form_valid(self, form):
        """Добавление автора к товару"""
        self.object = form.save()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductDetailView(DetailView):
    """Контроллер страницы товара по id"""
    model = Product


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self._get_formset()
        return context

    def _get_formset(self):
        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            return FormSet(self.request.POST, instance=self.object)
        return FormSet(instance=self.object)

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return self.form_invalid(form)

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        if self.request.user == self.get_object().author or self.request.user.is_superuser is True:
            return True
        return self.handle_no_permission()
