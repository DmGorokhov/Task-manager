from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.labels.models import Label


# Create your models here.
class Task(models.Model):
    name = models.CharField(_('Name'), max_length=255,
                            blank=False, null=False, unique=True)
    description = models.TextField(_('description'), blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                               related_name='author',
                               verbose_name=_('author')
                               )
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='status',
                               verbose_name=_('status')
                               )
    executor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT,
                                 null=True, blank=True,
                                 related_name='executor',
                                 verbose_name=_('executor')
                                 )

    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    labels = models.ManyToManyField(Label, through='TaskLabel',
                                    related_name='labels',
                                    verbose_name=_('labels'), blank=True,
                                    )

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
