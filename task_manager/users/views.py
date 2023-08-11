from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm, UserUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from .models import SiteUser
from task_manager.mixins.mixins import (LoginRequiredMixinWithFlash,
                                        IsOwnerOnlyMixin)


# Create your views here.

class UsersListView(ListView):
    model = SiteUser
    context_object_name = 'users_list'
    template_name = 'users/users_index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('date_joined')


class UserCreateView(SuccessMessageMixin, CreateView):
    model = SiteUser
    template_name = 'users/user_create.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    success_message = _("User is successfully registered")


class UserUpdateView(LoginRequiredMixinWithFlash, IsOwnerOnlyMixin,
                     SuccessMessageMixin, UpdateView):
    model = SiteUser
    template_name = 'users/user_update.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:users_list')
    success_message = _('User is successfully updated')


class UserDeleteView(LoginRequiredMixinWithFlash, IsOwnerOnlyMixin,
                     SuccessMessageMixin, DeleteView):
    model = SiteUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users:users_list')
    success_message = _('User is successfully deleted')
