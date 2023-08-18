from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginRequiredMixinWithFlash(LoginRequiredMixin):
    error_message = _("You are logged out")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(self.request, self.error_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class IsOwnerOnlyMixin(UserPassesTestMixin):
    err_message = _("You have no rights to change another user.")
    error_redirect_url = "users:users_list"

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.err_message)
        return redirect(reverse_lazy(self.error_redirect_url))


class DeleteProtectedMixin:
    rejection_message = ''
    rejection_redirect_url = ''

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.rejection_message)
            return redirect(reverse_lazy(self.rejection_redirect_url))
