from django.db import models
from django.db.models import Q


class NoteManager(models.Manager):
    def filter_notes(self, method=None, status=None, search=None, customer=None):
        if customer:
            qs = self.get_queryset().filter(customer=customer)
        else:
            qs = self.get_queryset()
        
        if method:
            qs = qs.filter(method=method)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(customer__first_name__icontains=search) |
                Q(customer__last_name__icontains=search) |
                Q(summary__icontains=search)
            )
        return qs