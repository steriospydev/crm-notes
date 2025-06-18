from django.urls import path
from .views import create_contact

app_name = 'contact'

urlpatterns = [   
    path('contacts/create/', create_contact, name='contact-create'),
    ]