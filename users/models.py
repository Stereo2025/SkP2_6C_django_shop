from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import string
import random


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Примерная реализация создания обычного пользователя
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def generate_secure_password(self, length=12):
        if length < 3:  # Базовая проверка, чтобы исключить слишком короткие пароли
            raise ValueError("Password length should be at least 4 characters")

        # Наборы символов
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        punctuation = string.punctuation

        # Строим пароль
        password = [
            random.choice(lower),
            random.choice(upper),
            random.choice(digits),
            random.choice(punctuation)
        ]

        # Дополняем до нужной длины
        password += random.choices(lower + upper + digits + punctuation, k=length - 4)

        # Перемешиваем
        random.shuffle(password)

        # Возвращаем в виде строки
        return ''.join(password)


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    verify_code = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    _is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self._is_staff

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

