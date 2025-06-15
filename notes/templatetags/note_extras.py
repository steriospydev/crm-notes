from django import template

register = template.Library()

@register.filter
def split_sentences(value):
    if not value:
        return []
    return [s.strip() for s in value.split(',') if s.strip()]
