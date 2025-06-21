from django.core.management.base import BaseCommand
from contact.models import Contact
from django.contrib.auth import get_user_model
from faker import Faker
import random


User = get_user_model()

fake = Faker('el_GR')  # Greek locale

class Command(BaseCommand):
    help = 'Generate 200 fake Greek contacts'

    def handle(self, *args, **options):
        created = 0
        for _ in range(30000):
            first_name = fake.first_name()
            last_name = fake.last_name()
            company = fake.company() if random.choice([True, False]) else None
            email = fake.email()
            tin_number = fake.unique.numerify(text='#########')  # 9-digit TIN
            phone_number = fake.numerify(text='69########')  # Mobile-like number
            summary_sentences = fake.text(max_nb_chars=200).split('. ')
            summary = ', '.join(sentence.strip().rstrip('.') for sentence in summary_sentences if sentence)

            try:
                Contact.objects.create(
                    user=User.objects.first(),
                    first_name=first_name,
                    last_name=last_name,
                    company=company,
                    email=email,
                    tin_number=tin_number,
                    phone_number=phone_number,
                    summary=summary
                )
                created += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Skipped contact due to error: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created} contacts'))
