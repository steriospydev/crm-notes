from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'company', 'email',
            'phone_number', 'tin_number', 'summary'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input',
                                                 'id' :'first_name',
                                                  'placeholder': 'Όνομα'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 
                                                'id' :'last_name','placeholder': 'Επίθετο'}),
            'company': forms.TextInput(attrs={'class': 'form-input',
                                              'id' :'company', 'placeholder': 'Εταιρία'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input',
                                                   'id' :'phone_number', 'placeholder': 'Τηλέφωνο'}),
            'email': forms.TextInput(attrs={'class': 'form-input',
                                            'id' :'email', 'placeholder': 'Email'}),
            'tin_number': forms.TextInput(attrs={'class': 'form-input input_style',
                                                 'id' :'tin_number',
                                                  'placeholder': 'ΑΦΜ'}),
            'summary': forms.Textarea(attrs={'class': 'form-input', 
                                             'id' :'summary',
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