from django import template

register = template.Library()

@register.filter
def show_default(value, default="--Κενό--"):
    if value is None or value == '':
        return default
    return value
