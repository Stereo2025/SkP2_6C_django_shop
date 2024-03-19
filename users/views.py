import random
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.shortcuts import redirect
from config.settings import EMAIL_HOST_USER
from users.forms import RegisterForm, UserForm
from users.models import User
from django.contrib.messages.views import SuccessMessageMixin


class LoginUserView(LoginView):
    template_name = 'users/login.html'


class LogoutUserView(LogoutView):
    pass


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def get_success_message(self, cleaned_data):
        return 'Вам на почту отправлено письмо, для прохождения верификации перейдите по ссылку в письме'

    def form_valid(self, form):
        new_user = form.save()
        code = ''.join(random.sample('0123456789', 5))
        new_user.verify_code = code
        new_user.is_active = False
        new_user.save()
        send_mail(
            'Верификация',
            f'Перейдите по ссылке для верификации: http://127.0.0.1:8000/users/verification/{code}',
            EMAIL_HOST_USER,
            [new_user.email]
        )
        return super().form_valid(form)


def verification(request, code):
    user = User.objects.get(verify_code=code)
    user.is_active = True
    user.verify_code = None  # Обнуляем или удаляем использованный код
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('catalog:home_page')

    def get_object(self, queryset=None):
        return self.request.user


def generate_password(request):
    new_password = User.objects.make_random_password()
    request.user.set_password(new_password)
    request.user.save()
    send_mail(
        'Смена пароля',
        f'Ваш новый пароль для авторизации: {new_password}',
        EMAIL_HOST_USER,
        [request.user.email]
    )
    messages.success(request, 'Вам на почту отправлено письмо с новым паролем для вашего аккаунта')
    return redirect(reverse('users:login'))