from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from tools.views import NoteFormListView

from .models import Note

   
class NotesIndexView(NoteFormListView):
    
    def get_queryset(self):
        method = self.request.GET.get('method')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        user = self.request.user

        return Note.lookfors.select_related('contact', 'user').filter_notes(
            user=user, method=method, status=status, search=search
            )


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
        # self.note_instance = get_object_or_404(Note, pk=self.kwargs['pk'])
        self.note_instance = get_object_or_404(Note.objects.select_related('contact', 'user'),
                                                pk=self.kwargs['pk'])
        if self.note_instance.user != request.user:
            messages.error(request, "Δεν έχετε άδεια να επεξεργαστείτε αυτή τη σημείωση.")
            return redirect('notes:index')
        
        
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        method = self.request.GET.get('method')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        return Note.lookfors.filter_notes(
            user=self.request.user,
            method=method,
            contact=self.note_instance.contact,
            status=status,
            search=search
            ).select_related('contact', 'user').order_by('-created')
        
        

    def get_success_url(self):
        return reverse_lazy('notes:note-update', kwargs={'pk': self.note_instance.pk})

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form = self.get_form()
    
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    


@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    # Ensure only the owner can delete
    if note.user != request.user:
        messages.error(request, "Δεν έχετε δικαίωμα να διαγράψετε αυτή τη σημείωση.")
        return redirect('notes:index')

    if request.method == 'POST':
        note.delete()
        messages.success(request, "Η σημείωση διαγράφηκε με επιτυχία.")
        return redirect('notes:index')

    messages.warning(request, "Η διαγραφή πρέπει να γίνει μέσω POST αιτήματος.")
    return redirect('notes:index')

