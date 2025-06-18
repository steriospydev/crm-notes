from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import  redirect

from .forms import ContactForm
# Create your views here.
@login_required
def create_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            messages.success(request, 'Η επαφή δημιουργήθηκε με επιτυχία.')
            return redirect('notes:index')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

            return redirect('notes:index')
    else:
        return redirect('notes:index')