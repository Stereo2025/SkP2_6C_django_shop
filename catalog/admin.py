from django.contrib import admin
from catalog.models import Product, Category, Contact, Blog, Version


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


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published', 'date_added',
                    'views_count', 'image')


@admin.register(Version)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')