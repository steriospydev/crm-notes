from django import forms
from .models import Note, Contact

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
                'rows': 6,
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

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'company', 'email',
            'phone_number', 'tin_number', 'summary'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Όνομα'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Επίθετο'}),
            'company': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Εταιρία'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Τηλέφωνο'}),
            'email': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'tin_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ΑΦΜ'}),
            'summary': forms.Textarea(attrs={'class': 'form-input', 
                                             'rows': 3,
                                             'placeholder': 'Περιγραφή'}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance