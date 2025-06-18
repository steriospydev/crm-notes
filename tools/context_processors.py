# crm/context_processors.py

from .models import PersonalTheme

def theme(request):
    return {
        "theme": PersonalTheme.get_solo()
    }
