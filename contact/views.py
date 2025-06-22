from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Contact
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
    


class ContactFormListView(LoginRequiredMixin, FormMixin, ListView):

    model = Contact
    template_name = 'contact/index.html' 
    context_object_name = 'contacts'
    paginate_by = 6
    form_class = ContactForm
    contact_instance = None  

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            return self.form_class(self.request.POST, instance=self.contact_instance)
        return self.form_class(instance=self.contact_instance)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['note_to_update'] = self.contact_instance        
        return context

    def form_valid(self, form):
        is_update = self.contact_instance is not None and self.contact_instance.pk is not None
        contact = form.save(commit=False)
        contact.user = self.request.user
        contact.save()

        if is_update:
            messages.success(self.request, 
                             f'Η επαφή: {contact } ενημερώθηκε με επιτυχία.')
        else:
            messages.success(self.request, 'Η επαφή δημιουργήθηκε με επιτυχία.')

        return super().form_valid(form)


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ContactIndexView(ContactFormListView):
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        user = self.request.user

        return Contact.objects.filter_contacts(
            user=user, search=search)


    def get_success_url(self):
        return reverse_lazy('contact:index')

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)


class ContactUpdateView(ContactFormListView):
    def dispatch(self, request, *args, **kwargs):
        # self.note_instance = get_object_or_404(Note, pk=self.kwargs['pk'])
        self.contact_instance = get_object_or_404(Contact, pk=self.kwargs['pk'])
        if self.contact_instance.user != request.user:
            messages.error(request, "Δεν έχετε άδεια να επεξεργαστείτε αυτή τη επαφή.")
            return redirect('contact:index')     
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Contact.objects.filter_contacts(
            user=self.request.user,
            search=search
            )
        
        

    def get_success_url(self):
        return reverse_lazy('contact:cntact-update', kwargs={'pk': self.contact_instance.pk})

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        form = self.get_form()
    
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)
    


