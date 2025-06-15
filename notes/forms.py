from django import forms
from .models import Note, Customer

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['customer', 'method', 'subject', 'summary', 'status']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={
                'class': 'form-control rounded rounded-3',
                'rows': 6,
                'placeholder': 'Πληκτρολογήστε τις σημειώσεις σας εδώ...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'father_name', 
            'phone_number', 'tin_number', 'summary'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Όνομα'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Επίθετο'}),
            'father_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Πατρώνυμο'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Τηλέφωνο'}),
            'tin_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ΑΦΜ'}),
            'summary': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Περιγραφή'}),
        }