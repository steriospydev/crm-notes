from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from .models import Note
from .forms import NoteForm
from django.contrib.auth.mixins import LoginRequiredMixin

class NotesIndexView(LoginRequiredMixin, FormMixin, ListView):
    model = Note
    template_name = 'index.html'
    context_object_name = 'notes'
    paginate_by = 6
    form_class = NoteForm

    def get_success_url(self):
        return reverse_lazy('notes:index')

    def get_queryset(self):
        return Note.objects.all().order_by('completed', '-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
