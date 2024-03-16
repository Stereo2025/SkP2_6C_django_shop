import psycopg2
from django.db import models
from django.db import connection


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