from django import template

register = template.Library()

@register.filter
def status_clas(status):
    return {
        'Ανοιχτό': 'open_class',
        'Κλειστό': 'close_class',
        'Σε Εξέλιξη': 'on_class'
    }.get(status, 'bg-secondary')

@register.filter
def status_icon(status):
    return {
        'Ανοιχτό': '<i class="bi bi-stop-circle-fill"></i>',
        'Κλειστό': '<i class="bi bi-check-lg"></i>',
        'Σε Εξέλιξη': '<i class="bi bi-arrow-clockwise"></i>'
    }.get(status, '<i class="bi bi-arrow-clockwise"></i>')