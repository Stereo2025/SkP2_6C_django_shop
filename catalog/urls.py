from catalog.views import home_page, contact
from django.urls import path

urlpatterns = [
    path('', home_page),
    path('contacts/', contact)
]
