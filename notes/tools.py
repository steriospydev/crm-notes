from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Note
from .forms import NoteForm, CustomerForm

class NoteFormListView(LoginRequiredMixin, FormMixin, ListView):
    model = Note
    template_name = 'index.html' 
    context_object_name = 'notes'
    paginate_by = 6
    form_class = NoteForm
    note_instance = None  

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            return self.form_class(self.request.POST, instance=self.note_instance,  user=self.request.user)
        return self.form_class(instance=self.note_instance, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['note_to_update'] = self.note_instance
        context['customer_form'] = CustomerForm() 
        return context

    def form_valid(self, form):
        is_update = self.note_instance is not None and self.note_instance.pk is not None
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()

        if is_update:
            messages.success(self.request, 
                             f'Η σημείωση του {note.customer } ενημερώθηκε με επιτυχία.')
        else:
            messages.success(self.request, 'Η σημείωση δημιουργήθηκε με επιτυχία.')

        return super().form_valid(form)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
