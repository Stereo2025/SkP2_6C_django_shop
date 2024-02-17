from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['categories']

    @staticmethod
    def json_read_products(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data['products']

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте список для хранения объектов категорий
        category_for_create = []

        # Создание категорий
        for category_data in Command.json_read_categories('fixtures/catalog_data.json'):
            category_for_create.append(
                Category(name=category_data['name'])
            )

        # Создание объектов Category в базе данных
        Category.objects.bulk_create(category_for_create)

        # Создание объектов продуктов
        product_for_create = []

        # Создание продуктов
        for product_data in Command.json_read_products('fixtures/catalog_data.json'):
            product_for_create.append(
                Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    category=Category.objects.get(name=product_data['category'])
                )
            )

        # Создание объектов Product в базе данных
        Product.objects.bulk_create(product_for_create)
