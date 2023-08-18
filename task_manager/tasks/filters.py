import django_filters
from .models import Task
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _
from django.forms import CheckboxInput


class TaskFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels',
        label=_('Label')
    )

    user_self_tasks = django_filters.BooleanFilter(
        field_name='author',
        label=_('Show only my tasks'),
        method='filter_self_user_tasks',
        widget=CheckboxInput
    )

    class Meta:
        model = Task
        fields = ['status', 'executor']

    def filter_self_user_tasks(self, queryset, author, value):
        current_user = self.request.user.pk
        if value:
            return queryset.filter(author=current_user)
        return queryset
