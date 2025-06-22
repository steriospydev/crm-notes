from tools.manager import UserOwnedManager, UserOwnedQuerySet
from django.db.models import Q


class ContactQuerySet(UserOwnedQuerySet):
    
    def filter_contacts(self, user, search=None):
        """
        Filter notes *owned by the given user* with additional filters.
        """
        qs = self.owned_by(user)
        if search:
            qs = qs.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(company__icontains=search)
            )
        return qs
    

    
    
class ContactManager(UserOwnedManager):
    queryset_class = ContactQuerySet
    
    def filter_contacts(self, *args, **kwargs):
        return self.get_queryset().filter_contacts(*args, **kwargs)


