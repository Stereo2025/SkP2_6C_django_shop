from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from catalog.forms import VersionForm, ProductForm, ModeratorProductForm
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


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView, PermissionRequiredMixin):
    model = Product

    def get_success_url(self):
        return reverse_lazy('catalog:products')

    def test_func(self):
        custom_perms = (
            'catalog.set_is_published',
            'catalog.set_category',
            'catalog.set_description'
        )
        user = self.request.user
        if user == self.get_object().author or user.is_superuser:
            return True
        if user.groups.filter(name='moderators').exists() and user.has_perms(custom_perms):
            return True
        return False

    def is_user_moderator(self):
        """Проверяет, входит ли пользователь в группу 'moderators'."""
        return self.request.user.groups.filter(name='moderators').exists()

    def get_form_class(self):
        if self.is_user_moderator():
            return ModeratorProductForm
        return ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Version, form=VersionForm, extra=1)
        context_data['formset'] = FormSet(self.request.POST or None, instance=self.object)
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context.get('formset')
        if formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        if self.request.user == self.get_object().author or self.request.user.is_superuser is True:
            return True
        return self.handle_no_permission()
