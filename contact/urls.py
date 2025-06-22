from django.urls import path
from .views import create_contact, ContactIndexView, ContactUpdateView

app_name = 'contact'

urlpatterns = [   
    path('', ContactIndexView.as_view(), name='index'),
    path('contact/update/<uuid:pk>/', ContactUpdateView.as_view(), name='contact-update'),
    path('create/', create_contact, name='contact-create'),
    
    ]