from django import template
from django.contrib.auth.models import Group

register = template.Library()


@register.filter
def mediapath(value):
    return '/media/' + str(value)


@register.simple_tag
def mediapath(value):
    return '/media/' + str(value)


@register.filter(name='moderators')
def moderators(user, group_name):
    try:
        group = Group.objects.get(name=group_name)
        return group in user.groups.all()
    except Group.DoesNotExist:
        return False
