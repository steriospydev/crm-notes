from django import forms
from contact.models import Contact

from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['contact', 'method', 'subject', 'summary', 'status']
        widgets = {
            'contact': forms.Select(attrs={'class': 'form-select'}),
            'method': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'summary': forms.Textarea(attrs={
                'class': 'form-control rounded rounded-3',
                'rows': 3,
                'placeholder': 'Πληκτρολογήστε τις σημειώσεις σας εδώ...'
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Accept user in constructor
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['contact'].queryset = Contact.objects.owned_by(user)
        else:
            self.fields['contact'].queryset = Contact.objects.none()
