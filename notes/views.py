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
        return Note.objects.all().order_by('completed', '-created')

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
    

# I want to create the same page for Update view of a Note, the form will contain
# the object's values to be updated while the List will contain all notes with the same customer value  e.g url /notes/1 
# class NotesIndexView(LoginRequiredMixin, FormMixin, ListView):
#     model = Note
#     template_name = 'index.html'
#     context_object_name = 'notes'
#     paginate_by = 6
#     form_class = NoteForm

#     def get_success_url(self):
#         return reverse_lazy('notes:index')

#     def get_queryset(self):
#         return Note.objects.all().order_by('completed', '-created')

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if 'form' not in context:
#             context['form'] = self.get_form()
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object_list = self.get_queryset()
#         form = self.get_form()
#         if form.is_valid():
#             form.save()
#             return self.form_valid(form)
#         return self.form_invalid(form)

#     def form_valid(self, form):
#         note = form.save(commit=False)
#         note.user = self.request.user
#         note.save()
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))
