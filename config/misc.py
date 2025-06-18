import uuid
from django.db import models
from django.core.validators import RegexValidator

class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

TIN_REGEX = RegexValidator(regex=r'^\d{9}$', message="Το ΑΦΜ πρέπει να έχει 9 ψηφία.")
PHONE_REGEX = RegexValidator(regex=r'^\d{10}$', message="Το τηλέφωνο πρέπει να έχει 10 ψηφία.")
EMAIL_REGEX = RegexValidator(regex=r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+',
                             message="Wrong email Format.")

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