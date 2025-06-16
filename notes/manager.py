from django.db import models
from django.db.models import Q
from django.core.exceptions import PermissionDenied


class CustomerQuerySet(models.QuerySet):
    def owned_by(self, user):
        if not user or not user.is_authenticated:
            raise PermissionDenied("A valid user is required to access these customers.")
        return self.filter(user=user)


class NoteQuerySet(models.QuerySet):
    def owned_by(self, user):
        if not user or not user.is_authenticated:
            raise PermissionDenied("A valid user is required to access these notes.")
        return self.filter(user=user)

    def filter_notes(self, user, method=None, status=None, search=None, customer=None):
        """
        Filter notes *owned by the given user* with additional filters.
        """
        qs = self.owned_by(user)

        if customer:
            qs = qs.filter(customer=customer)
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
    
class NoteManager(models.Manager):
    def get_queryset(self):
        return NoteQuerySet(self.model, using=self._db)

    def filter_notes(self, *args, **kwargs):
        return self.get_queryset().filter_notes(*args, **kwargs)

class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)

    def owned_by(self, user):
        return self.get_queryset().owned_by(user)
