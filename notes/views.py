from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib import messages
from .models import Note
from .tools import NoteFormListView


from .forms import CustomerForm

@login_required
def create_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # assign user here
            customer.save()
            messages.success(request, 'Ο πελάτης δημιουργήθηκε με επιτυχία.')
            return redirect('notes:index')  # your index view's URL name
        else:
            for error in form.non_field_errors():
                messages.error(request, error)

            return redirect('notes:index')
    else:
        return redirect('notes:index')


class NotesIndexView(NoteFormListView):
    def get_queryset(self):
        method = self.request.GET.get('method')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        return Note.lookfors.filter_notes(method=method, status=status, search=search)

    def get_success_url(self):
        return reverse_lazy('notes:index')

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class NoteUpdateView(NoteFormListView):
    def dispatch(self, request, *args, **kwargs):
        self.note_instance = get_object_or_404(Note, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter notes by same customer
        return Note.objects.filter(customer=self.note_instance.customer).order_by('-created')

    def get_success_url(self):
        return reverse_lazy('notes:note-update', kwargs={'pk': self.note_instance.pk})

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    