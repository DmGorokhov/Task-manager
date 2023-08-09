from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class HomeView(TemplateView):
    template_name = 'home.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "registration/login.html"
    success_message = _("You are logged in")


class UserLogoutView(SuccessMessageMixin, LogoutView):
    def get_default_redirect_url(self):
        messages.info(self.request, _('You are logged out'))
        return super().get_default_redirect_url()
