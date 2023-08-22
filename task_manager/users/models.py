from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.models import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class SiteUserManage(UserManager):

    def create_user(self, username, email=None, password=None,
                    first_name=None, last_name=None, **extra_fields):
        """
        Override build-in method for
        add last_name and first_name ad required fields
        """
        if not first_name or not last_name:
            raise ValueError("The first_name and last_name must be set")
        extra_fields['first_name'] = first_name
        extra_fields['last_name'] = last_name
        return super().create_user(username, email, password, **extra_fields)


class SiteUser(AbstractUser):
    """Model representing a user account."""
    first_name = models.CharField(_('first name'), max_length=30,
                                  blank=False, null=False)
    last_name = models.CharField(_('last name'), max_length=150,
                                 blank=False, null=False)

    objects = SiteUserManage()

    def __str__(self):
        """Represent an instance as a string."""
        return self.get_full_name()
