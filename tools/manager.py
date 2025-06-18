from django.db import models
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