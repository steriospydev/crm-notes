from django.db import models
from django.contrib.auth import get_user_model
from tools.constants import TIN_REGEX, PHONE_REGEX, EMAIL_REGEX
from tools.models import TimeStampedModel
from .manager import ContactManager

# Create your models here.
User = get_user_model()

class Contact(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                              verbose_name='Χρήστης', null=True, blank=True)
    first_name = models.CharField('Ονομα', max_length=155)
    last_name = models.CharField('Επίθετο', max_length=155)
    company = models.CharField('Οντότητα', max_length=155, blank=True, null=True)
    email = models.CharField('Email',
                             max_length=200,
                             blank=True,null=True,
                             validators=[EMAIL_REGEX])
    tin_number = models.CharField('ΑΦΜ', max_length=9, blank=True, null=True, 
                                  validators=[TIN_REGEX], unique=True)
    phone_number = models.CharField('Τηεφωνο', max_length=10, blank=True, null=True, validators=[PHONE_REGEX])
    summary = models.TextField('Πληροφορίες', blank=True, null=True)

    objects = ContactManager()
    
    class Meta:
        verbose_name = 'Επαφή'
        verbose_name_plural = 'Επαφές'
        unique_together = ['first_name', 'last_name', 'company', 'user']

    def __str__(self):
        fullname = f'{self.first_name} {self.last_name}'
        display = f'{fullname} - {self.company}' if self.company else fullname
        return display
