from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from blog.models import Blog
from pytils.translit import slugify
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from django.urls import reverse_lazy, reverse


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
        if self.object.views_count == 100:
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
    success_url = reverse_lazy('blog:articles')

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
        new_article = form.save()
        new_article.slug = slugify(new_article.title)
        new_article.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.object.slug])


class ArticleDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:articles')
