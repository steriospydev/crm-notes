from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from contact.models import Contact
from notes.models import Note
from tools.constants import STATUS_CHOICES, SUBJECT_CHOICES, COMMUNICATION_METHODS

from faker import Faker
import random

fake = Faker('el_GR')
User = get_user_model()

class Command(BaseCommand):
    help = 'Generate 5 notes for each contact with weighted statuses'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('No user found in the database.'))
            return

        contacts = Contact.objects.all()
        if not contacts.exists():
            self.stdout.write(self.style.ERROR('No contacts found.'))
            return

        # Map status values
        status_labels = [choice[0] for choice in STATUS_CHOICES]
        subject_labels = [choice[0] for choice in SUBJECT_CHOICES]
        method_labels = [choice[0] for choice in COMMUNICATION_METHODS]

        # Weight the statuses: 60% Κλειστό, 20% Ανοιχτό, 20% Σε εξέλιξη
        status_choices = (
            [label for label in status_labels if label == 'Κλειστό'] * 60 +
            [label for label in status_labels if label == 'Ανοιχτό'] * 20 +
            [label for label in status_labels if label == 'Σε εξέλιξη'] * 20
        )

        total_created = 0

        for contact in contacts:
            for _ in range(5):
                summary_sentences = fake.text(max_nb_chars=200).split('. ')
                summary = ', '.join(sentence.strip().rstrip('.') for sentence in summary_sentences if sentence)
                Note.objects.create(
                    user=user,
                    contact=contact,
                    subject=random.choice(subject_labels),
                    method=random.choice(method_labels),
                    status=random.choice(status_choices),
                    summary=summary
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total_created} notes.'))
