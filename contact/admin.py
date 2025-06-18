from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'company', 'tin_number', 'phone_number', 'id']

