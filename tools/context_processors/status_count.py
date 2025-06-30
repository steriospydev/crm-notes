from django.db.models import Count
from notes.models import Note

def status_counts(request):
    if not request.user.is_authenticated:
        return {}

    # Get status choices from the model (value, label)
    status_choices = Note._meta.get_field('status').choices

    # Count how many notes exist per status for the current user
    counts = (
        Note.objects
        .filter(user=request.user)
        .values('status')
        .annotate(count=Count('id'))
    )

    # Make a dictionary: {'Ανοιχτό': 12, 'Κλειστό': 4, ...}
    count_dict = {item['status']: item['count'] for item in counts}

    # Build result list with correct label from choices and only if count > 0
    result = [
        {'label': label, 'value': count}
        for status, label in status_choices
        if (count := count_dict.get(status))  # Only include if there's a count
    ]

    return {'status_counts': result}
