from django.db import models


# Create your models here.
class Product(models.Model):

    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=500, verbose_name='Описание')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Превью')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='Дата изменения')
    price = models.IntegerField(verbose_name='Цена', default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Category(models.Model):

    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
