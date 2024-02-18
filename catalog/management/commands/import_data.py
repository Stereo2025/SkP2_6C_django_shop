from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json
from django.db import transaction


class Command(BaseCommand):

    def import_categories(self, entries):
        for entry in entries:
            #  Проходимся по всем записям и проверяем, относится ли данная запись к модели catalog.category.
            if entry['model'] == 'catalog.category':
                # Создаем объект категории, используя значения из словаря. entry['pk'] используется как идентификатор
                # объекта, а **entry['fields'] распаковывает остальные поля из записи
                Category.objects.create(
                    id=entry['pk'],
                    **entry['fields']
                )

    def import_products(self, entries):
        for entry in entries:
            #  Проходимся по всем записям и проверяем, относится ли данная запись к модели product.
            if entry['model'] == 'catalog.product':
                product_data = entry['fields']
                # Предполагаем, что категории уже импортированы и существуют.
                product_data['category'] = Category.objects.get(pk=product_data['category'])
                # Извлекаем данные продукта из записи. Затем заменяем идентификатор категории на соответствующий объект
                # категории, полученный из базы данных.
                Product.objects.create(
                    id=entry['pk'],
                    **product_data
                )
    # Создаем объект продукта с помощью извлеченных данных
    def handle(self, *args, **options):
        file_path = 'fixtures/catalog_data.json'
        # Удаляем все существующие записи из таблиц продуктов и категорий перед импортом новых данных.
        self.stdout.write("Deleting existing data...")
        Product.objects.all().delete()
        Category.objects.all().delete()

        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                products_and_categories = json.load(file)
            # Начинаем атомарную транзакцию для обеспечения атомарности операции импорта данных.
            with transaction.atomic():
                # Сначала импортируем категории
                self.import_categories(products_and_categories)
                # Затем импортируем продукты
                self.import_products(products_and_categories)

            self.stdout.write(self.style.SUCCESS('Successfully imported data from JSON.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
