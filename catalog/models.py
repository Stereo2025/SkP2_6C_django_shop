from django.db import models
import psycopg2
from django.db import connection
from django.db.models.signals import post_save
from django.dispatch import receiver


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

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        app_label = 'catalog'


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.TextField(max_length=500, verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        app_label = 'catalog'


class Contact(models.Model):
    """Модель таблицы - контакты"""
    name = models.CharField(max_length=150, verbose_name='Имя')
    email = models.EmailField(max_length=150, verbose_name='Почта')
    post = models.CharField(max_length=150, verbose_name='Должность')

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class Blog(models.Model):
    """Модель таблицы - товары"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, blank=True, null=True, verbose_name='slug')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Превью')
    content = models.TextField(max_length=1000, verbose_name='Содержимое')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    date_added = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    def __str__(self):
        return f'{self.title}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Version(models.Model):
    """Модель таблицы - версия"""
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    name = models.CharField(max_length=150, verbose_name='Название версии')
    number = models.FloatField(verbose_name='Номер версии')

    is_active = models.BooleanField(default=False, verbose_name='Активна')

    @classmethod
    def truncate_table_restart_id(cls):
        """Метод для обнуления счетчика автоинкремента"""

        with connection.cursor() as cur:
            try:
                cur.execute(f'TRUNCATE TABLE {cls._meta.db_table} RESTART IDENTITY CASCADE')
            except psycopg2.errors.Error as e:
                raise e

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс отображения метаданных"""
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'


@receiver(post_save, sender=Version)
def set_active_version(sender, instance, **kwargs):
    update_fields = kwargs.get('update_fields', [])
    if update_fields is not None and 'is_active' in update_fields and instance.is_active:
        Version.objects.filter(product=instance.product).exclude(pk=instance.pk).update(is_active=False)
