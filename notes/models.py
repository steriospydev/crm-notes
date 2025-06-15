import uuid
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

TIN_REGEX = RegexValidator(regex=r'^\d{9}$', message="Το ΑΦΜ πρέπει να έχει 9 ψηφία.")
PHONE_REGEX = RegexValidator(regex=r'^\d{10}$', message="Το τηλέφωνο πρέπει να έχει 10 ψηφία.")


class Customer(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης', null=True, blank=True)
    first_name = models.CharField('Ονομα', max_length=155)
    last_name = models.CharField('Επίθετο', max_length=155)
    father_name = models.CharField('Πατρώνυμο', max_length=155, blank=True, null=True)
    tin_number = models.CharField('ΑΦΜ', max_length=9, blank=True, null=True, validators=[TIN_REGEX])
    phone_number = models.CharField('Τηεφωνο', max_length=10, blank=True, null=True, validators=[PHONE_REGEX])

    class Meta:
        verbose_name = 'Αγροτης'
        verbose_name_plural = 'Αγροτες'

    def __str__(self):
        return f'{self.first_name} {self.last_name} του {self.father_name}'



class Note(TimeStampedModel):
    COMMUNICATION_METHODS = [
    ('Τηλέφωνο', 'Τηλέφωνο'),
    ('Γραφείο', 'Γραφείο'),
    ('Email', 'Email'),
    ('Έγγραφο', 'Έγγραφο'),
    ('Άλλο', 'Άλλο'),
]

    STATUS_CHOICES = [
    ('Ανοιχτό', 'Ανοιχτό'),
    ('Σε Εξέλιξη', 'Σε Εξέλιξη'),
    ('Κλειστό', 'Κλειστό'),
]
    SUBJECT_CHOICES = [
    ('Άλλο', 'Άλλο'),
    ('Πληρωμή', 'Πληρωμή'),
    ('Αρδευτική Ενημερότητα', 'Αρδευτική Ενημερότητα'),
    ('Εύρεση Αγροτεμαχίου', 'Εύρεση Αγροτεμαχίου'),
    ('Λογαριασμός', 'Λογαριασμός'),
    ('Τιμολόγιο', 'Τιμολόγιο'),
    ('Ενημέρωση', 'Ενημέρωση'),
    ('Αποζημίωση', 'Αποζημίωση'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Χρήστης', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='notes',
                                  verbose_name='Επαφή')
    method = models.CharField('Επικοινωνία', max_length=20,
                               choices=COMMUNICATION_METHODS, default='Γραφείο')
    subject = models.CharField('Θεμα', max_length=255, choices=SUBJECT_CHOICES, 
                               default='Άλλο')
    summary = models.TextField('Περιληψη', blank=True, null=True)
    status = models.CharField('Κατασταση', max_length=20, choices=STATUS_CHOICES,
                               default='ΑΝΟΙΧΤΟ')
    completed = models.BooleanField('ολοκληρωθηκε', default=False)

    class Meta:
        verbose_name = 'Σημειωση'
        verbose_name_plural = 'Σημειωσεις'
        ordering = ['-created']

    def __str__(self):
        return f'{self.created.date()} - {self.customer}- {self.status}'
    
 
    def save(self, *args, **kwargs):
        # Update `completed` based on status
        if self.status == 'Κλειστό':
            self.completed = True
        else:
            self.completed = False

        super().save(*args, **kwargs)