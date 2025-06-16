from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from config.misc import (TimeStampedModel, TIN_REGEX, PHONE_REGEX,
                         STATUS_CHOICES, SUBJECT_CHOICES, COMMUNICATION_METHODS)


from .manager import NoteManager, CustomerManager

User = get_user_model()

class Customer(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='Χρήστης', null=True, blank=True)
    first_name = models.CharField('Ονομα', max_length=155)
    last_name = models.CharField('Επίθετο', max_length=155)
    father_name = models.CharField('Πατρώνυμο', max_length=155, blank=True, null=True)
    tin_number = models.CharField('ΑΦΜ', max_length=9, blank=True, null=True, validators=[TIN_REGEX])
    phone_number = models.CharField('Τηεφωνο', max_length=10, blank=True, null=True, validators=[PHONE_REGEX])
    summary = models.CharField('ΠΛηροφορίες', max_length=240, blank=True, null=True)

    objects = CustomerManager()
    
    class Meta:
        verbose_name = 'Επαφή'
        verbose_name_plural = 'Επαφές'
        unique_together = ['first_name', 'last_name', 'father_name', 'user']

    def __str__(self):
        return f'{self.first_name} {self.last_name} του {self.father_name}'


class Note(TimeStampedModel):       
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='notes',
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
        return f'{self.created.date()} - {self.customer}- {self.status}'
    
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
