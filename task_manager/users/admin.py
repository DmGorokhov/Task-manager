from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin

from .models import SiteUser


class SiteUserAdmin(UserAdmin):
    model = SiteUser
    add_form = UserCreationForm
    form = UserChangeForm
    add_fieldsets = (
        (None, {'fields': ('first_name', 'last_name',
                           'username', 'password1', 'password2')
                }),
    )


admin.site.register(SiteUser, SiteUserAdmin)
