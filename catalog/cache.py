from django.conf import settings
from django.core.cache import cache
from catalog.models import Category


def get_categories_from_cache():
    if getattr(settings, 'CACHE_ENABLED', False):
        key = 'categories'
        category_list = cache.get(key)
        if category_list is None:
            category_list = list(Category.objects.all())
            cache.set(key, category_list, timeout=3600)
    else:
        category_list = list(Category.objects.all())

    return category_list
