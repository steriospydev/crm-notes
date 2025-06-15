from django.urls import path
from .views import NotesIndexView    

app_name = 'notes'

urlpatterns = [
    path('', NotesIndexView.as_view(), name='index'),
  
]