from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (CreateView, UpdateView,
                                  DeleteView, DetailView)

from task_manager.mixins.mixins import (LoginRequiredMixinWithFlash,
                                        IsOwnerOnlyMixin)
from .filters import TaskFilter
from .forms import TaskForm
from .models import Task
from django_filters.views import FilterView


class TasksFilterView(LoginRequiredMixinWithFlash, FilterView):
    model = Task
    context_object_name = 'tasks_list'
    template_name = 'tasks/tasks_index.html'
    filterset_class = TaskFilter

    def get_queryset(self):
        return super().get_queryset().order_by('created_at')


class TaskCreateView(LoginRequiredMixinWithFlash,
                     SuccessMessageMixin, CreateView):
    model = Task
    template_name = 'tasks/task_create.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _("Task is successfully created")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixinWithFlash,
                     SuccessMessageMixin, UpdateView):
    model = Task
    template_name = 'tasks/task_update.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _("Task is successfully updated")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixinWithFlash, IsOwnerOnlyMixin,
                     SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks:tasks_list')
    success_message = _('Task is successfully deleted')
    err_message = _("A task can only be deleted by its author.")
    error_redirect_url = "tasks:tasks_list"

    def test_func(self):
        return self.get_object().author == self.request.user


class TaskDetailView(LoginRequiredMixinWithFlash, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
