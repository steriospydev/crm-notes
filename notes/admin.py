from django.contrib import admin
from .models import Contact, Note

@admin.register(Contact)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'tin_number', 'phone_number', 'id']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'contact', 'method', 'subject', 'status', 'user', 'created'
    ]
    list_editable = ['status', 'method', 'subject', 'user']
    list_filter = ['subject', 'status']

