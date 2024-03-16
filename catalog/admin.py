from django.contrib import admin
from catalog.models import Product, Category, Contact, Version #, Blog,


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')


@admin.register(Version)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')