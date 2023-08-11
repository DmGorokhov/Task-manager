from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from task_manager.mixins.mixins import LoginRequiredMixinWithFlash
from django.utils.translation import gettext_lazy as _

from .forms import StatusForm
from .models import Status


# Create your views here.
class StatusesListView(LoginRequiredMixinWithFlash, ListView):
    model = Status
    context_object_name = 'statuses_list'
    template_name = 'statuses/statuses_index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('created_at')


class StatusCreateView(LoginRequiredMixinWithFlash,
                       SuccessMessageMixin, CreateView):
    model = Status
    template_name = 'statuses/status_create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:statuses_list')
    success_message = _("Status is successfully created")


class StatusUpdateView(LoginRequiredMixinWithFlash,
                       SuccessMessageMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses:statuses_list')
    success_message = _("Status is successfully updated")


class StatusDeleteView(LoginRequiredMixinWithFlash,
                       SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses:statuses_list')
    success_message = _('Status is successfully deleted')
