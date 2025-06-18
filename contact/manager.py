from tools.manager import UserOwnedManager, UserOwnedQuerySet


class ContactQuerySet(UserOwnedQuerySet):
    pass
    
    
class ContactManager(UserOwnedManager):
    queryset_class = ContactQuerySet

