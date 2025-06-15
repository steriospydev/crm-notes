from django.contrib import admin
from .models import Customer, Note

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'father_name', 'tin_number', 'phone_number', 'id']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'method', 'subject', 'status', 'user', 'created'
    ]
    list_editable = ['status', 'method', 'subject', 'user']
    list_filter = ['subject', 'status']

