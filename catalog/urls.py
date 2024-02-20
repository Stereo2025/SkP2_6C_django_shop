from catalog.apps import CatalogConfig
from catalog.views import home_page, contacts, products, user_product, view_product
from django.urls import path

app_name = CatalogConfig.name

urlpatterns = [
    path('', home_page, name='home_page'),
    path('contacts/', contacts, name='contacts'),
    path('products/', products, name='products'),
    path('add/', user_product, name='user_product'),
    path('products/<int:pk>/', view_product, name='view_product')
]
