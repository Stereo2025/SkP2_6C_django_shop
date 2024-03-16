from django.urls import path

from blog.apps import BlogConfig
from blog.views import ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetailView

app_name = BlogConfig.name

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/create/', ArticleCreateView.as_view(), name='create'),
    path('articles/update/<str:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('articles/delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='view')
]