from django.urls import path
from django.views.decorators.cache import never_cache
from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/create/', never_cache(ArticleCreateView.as_view()), name='create'),
    path('articles/update/<str:slug>/', never_cache(ArticleUpdateView.as_view()), name='update'),
    path('articles/delete/<str:slug>/', never_cache(ArticleDeleteView.as_view()), name='delete'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='view')
]