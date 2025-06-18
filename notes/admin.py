from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'contact', 'method', 'subject', 'status', 'user', 'created'
    ]
    list_editable = ['status', 'method', 'subject', 'user']
    list_filter = ['subject', 'status']

