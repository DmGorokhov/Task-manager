from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView, ListView)
from task_manager.mixins.mixins import (LoginRequiredMixinWithFlash,
                                        DeleteProtectedMixin)
from django.utils.translation import gettext_lazy as _

from .forms import LabelForm
from .models import Label


# Create your views here.
class LabelsListView(LoginRequiredMixinWithFlash, ListView):
    model = Label
    context_object_name = 'labels_list'
    template_name = 'labels/labels_index.html'

    def get_queryset(self):
        return super().get_queryset().order_by('created_at')


class LabelCreateView(LoginRequiredMixinWithFlash,
                      SuccessMessageMixin, CreateView):
    model = Label
    template_name = 'labels/label_create.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:labels_list')
    success_message = _("Label is successfully created")


class LabelUpdateView(LoginRequiredMixinWithFlash,
                      SuccessMessageMixin, UpdateView):
    model = Label
    template_name = 'labels/label_update.html'
    form_class = LabelForm
    success_url = reverse_lazy('labels:labels_list')
    success_message = _("Label is successfully updated")


class LabelDeleteView(LoginRequiredMixinWithFlash,
                      SuccessMessageMixin, DeleteProtectedMixin,
                      DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels:labels_list')
    success_message = _('Label is successfully deleted')

    rejection_message = _("Can't delete label because it's in use")
    rejection_redirect_url = "labels:labels_list"
