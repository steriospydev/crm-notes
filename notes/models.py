from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
                         
from tools.models import TimeStampedModel
from tools.constants import STATUS_CHOICES, SUBJECT_CHOICES, COMMUNICATION_METHODS

from contact.models import Contact
from .manager import NoteManager


User = get_user_model()

class Note(TimeStampedModel):       
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης', null=True, blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name='notes',
                                  verbose_name='Επαφή')
    method = models.CharField('Επικοινωνία', max_length=20,
                               choices=COMMUNICATION_METHODS, default='Γραφείο')
    subject = models.CharField('Θεμα', max_length=255, choices=SUBJECT_CHOICES, 
                               default='Άλλο')
    summary = models.TextField('Περιληψη', blank=True, null=True)
    status = models.CharField('Κατασταση', max_length=20, choices=STATUS_CHOICES,
                               default='Ανοιχτό')
    completed = models.BooleanField('ολοκληρωθηκε', default=False)
    shortcode = models.CharField(max_length=10, unique=True, blank=True, null=True)

    objects = models.Manager() 
    lookfors = NoteManager()   

    class Meta:
        verbose_name = 'Σημειωση'
        verbose_name_plural = 'Σημειωσεις'
        ordering = ['-created']

    def __str__(self):
        return f'{self.created.date()} - {self.contact}- {self.status}'
    
    def get_absolute_url(self):
        return reverse('notes:note-update', kwargs={'pk': self.pk})
    
    def has_completed(self):
        if self.status != 'Κλειστό':
            return False
        return True
    
    def generate_shortcode(self):
        last_note = Note.objects.order_by('-created').first()
    
        if last_note and last_note.shortcode and last_note.shortcode.startswith("E-"):
            try:
                last_number = int(last_note.shortcode.split("-")[1])
            except (IndexError, ValueError):
                last_number = 0
        else:
            last_number = 0

        next_number = last_number + 1
        return f"E-00{next_number}"

    def save(self, *args, **kwargs):
        self.completed = self.has_completed()
        if not self.shortcode:
            self.shortcode = self.generate_shortcode()


        super().save(*args, **kwargs)
