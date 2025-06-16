from django.urls import path
from .views import NotesIndexView, NoteUpdateView, create_contact, delete_note

app_name = 'notes'

urlpatterns = [
    path('', NotesIndexView.as_view(), name='index'),
    path('note/update/<uuid:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('note/delete/<uuid:pk>/', delete_note, name='note-delete'),
    path('contacts/create/', create_contact, name='contact-create'),
    ]