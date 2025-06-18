from django.db.models import Q
from tools.manager import UserOwnedManager, UserOwnedQuerySet


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
    

class NoteManager(UserOwnedManager):
    queryset_class = NoteQuerySet

    def filter_notes(self, *args, **kwargs):
        return self.get_queryset().filter_notes(*args, **kwargs)
