from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
from django.db import transaction


class Command(BaseCommand):

    def import_categories(self, entries):
        for entry in entries:
            if entry['model'] == 'catalog.category':
                Category.objects.create(
                    id=entry['pk'],
                    **entry['fields']
                )

    def import_products(self, entries):
        for entry in entries:
            if entry['model'] == 'catalog.product':
                product_data = entry['fields']
                # Предполагаем, что категории уже импортированы и существуют.
                product_data['category'] = Category.objects.get(pk=product_data['category'])
                Product.objects.create(
                    id=entry['pk'],
                    **product_data
                )

    def handle(self, *args, **options):
        file_path = 'fixtures/catalog_data.json'

        self.stdout.write("Deleting existing data...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                products_and_categories = json.load(file)

            with transaction.atomic():
                # Сначала импортируем категории
                self.import_categories(products_and_categories)
                # Затем импортируем продукты
                self.import_products(products_and_categories)

            self.stdout.write(self.style.SUCCESS('Successfully imported data from JSON.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
