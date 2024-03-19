from django.urls import path
from users.apps import UsersConfig
from users.views import LoginUserView, LogoutUserView, RegisterUserView, verification, UserUpdateView, generate_password

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verification/<str:code>/', verification, name='verification'),
    path('profile/genpassword', generate_password, name='genpassword'),
    path('profile/', UserUpdateView.as_view(), name='profile')

]
