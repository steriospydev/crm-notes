from django.db import models
from django.db.models import Q
from django.core.exceptions import PermissionDenied


class UserOwnedQuerySet(models.QuerySet):
    def owned_by(self, user):
        if not user or not user.is_authenticated:
            raise PermissionDenied("A valid user is required to access these objects.")
        return self.filter(user=user)

class UserOwnedManager(models.Manager):
    def get_queryset(self):
        return self.queryset_class(self.model, using=self._db)

    def owned_by(self, user):
        return self.get_queryset().owned_by(user)
    
class ContactQuerySet(UserOwnedQuerySet):
    pass


class NoteQuerySet(UserOwnedQuerySet):

    def filter_notes(self, user, method=None, status=None, search=None, contact=None):
        """
        Filter notes *owned by the given user* with additional filters.
        """
        qs = self.owned_by(user)

        if contact:
            qs = qs.filter(contact=contact)
        if method:
            qs = qs.filter(method=method)
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(
                Q(contact__first_name__icontains=search) |
                Q(contact__last_name__icontains=search) |
                Q(summary__icontains=search)
            )
        return qs
    
    
class ContactManager(UserOwnedManager):
    queryset_class = ContactQuerySet

class NoteManager(UserOwnedManager):
    queryset_class = NoteQuerySet

    def filter_notes(self, *args, **kwargs):
        return self.get_queryset().filter_notes(*args, **kwargs)
