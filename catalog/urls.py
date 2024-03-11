from catalog.apps import CatalogConfig
from catalog.views import HomeListView, ContactTemplateView, ProductListView, ProductCreateView, ProductDetailView, \
    ProductUpdateView, ArticleListView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView, ArticleDetailView
from django.urls import path

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeListView.as_view(), name='home_page'),
    path('contacts/', ContactTemplateView.as_view(), name='contacts'),
    path('products/', ProductListView.as_view(), name='products'),
    path('add/', ProductCreateView.as_view(), name='user_product'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='view_product'),

    path('articles/', ArticleListView.as_view(), name='articles'),
    path('articles/create/', ArticleCreateView.as_view(), name='create'),
    path('articles/update/<str:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('articles/delete/<str:slug>/', ArticleDeleteView.as_view(), name='delete'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='view')
]
