from django.urls import path
from .views import NotesIndexView, NoteUpdateView, create_customer

app_name = 'notes'

urlpatterns = [
    path('', NotesIndexView.as_view(), name='index'),
    path('<uuid:pk>/update/', NoteUpdateView.as_view(), name='note-update'),

    path('customers/create/', create_customer, name='customer-create'),
    ]