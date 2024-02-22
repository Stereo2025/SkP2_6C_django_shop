from django import template

register = template.Library()


@register.filter
def mediapath(value):
    return '/media/' + str(value)


@register.simple_tag
def mediapath(value):
    return '/media/' + str(value)
