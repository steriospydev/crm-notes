import uuid
from django.db import models

# Create your models here.
class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class PersonalTheme(models.Model):
    bg_body = models.CharField(max_length=10, blank=True, null=True)
    bg_navbar = models.CharField(max_length=10, blank=True, null=True)
    bg_note = models.CharField(max_length=10, blank=True, null=True)
    text_note = models.CharField(max_length=10, blank=True, null=True)
    text_body = models.CharField(max_length=10, blank=True, null=True)
    text_navbar = models.CharField(max_length=10, blank=True, null=True)
    bg_form = models.CharField(max_length=10, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Always use primary key = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Prevent deletion

    @classmethod
    def get_solo(cls):
        return cls.objects.get_or_create(pk=1)[0]

    def __str__(self):
        return "Personal Theme Settings"