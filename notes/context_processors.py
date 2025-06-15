from django.contrib.auth.models import User
from .models import Note, Customer, User

def global_counts(request):
    return {
        'user_count': User.objects.count(),
        'note_count': Note.objects.count(),
        'customer_count': Customer.objects.count(),
    }
