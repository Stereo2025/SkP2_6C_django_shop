from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import os

User = get_user_model()


class Command(BaseCommand):
    help = 'Создает суперпользователя с указанным email и паролем'

    def add_arguments(self, parser):
        # Опциональный аргумент для ввода email
        parser.add_argument('--email', type=str, help='Email нового суперпользователя',
                            default='stereoletto@yandex.ru')

        # Опциональный аргумент для ввода пароля; если не указан - будет запрошен в runtime
        parser.add_argument('--password', type=str, help='Пароль нового суперпользователя')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password'] or os.getenv('SUPERUSER_PASSWORD')

        # Запрашиваем пароль, если он не предоставлен и не установлен через переменную окружения
        if not password:
            password = input('Введите пароль нового суперпользователя: ')

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'Пользователь с email {email} уже существует.'))
        else:
            user = User.objects.create_superuser(email=email, password=password)
            user.first_name = 'FirstName'
            user.last_name = 'LastName'
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Суперпользователь с email {email} успешно создан.'))
