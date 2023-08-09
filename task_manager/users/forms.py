from django.contrib.auth import forms

from .models import SiteUser


class UserCreationForm(forms.UserCreationForm):
    """Site user creation form."""

    class Meta(forms.UserCreationForm.Meta):
        model = SiteUser
        fields = ('first_name', 'last_name', 'username')


class UserUpdateForm(UserCreationForm):
    def clean_username(self):
        return self.cleaned_data.get("username")
