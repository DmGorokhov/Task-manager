from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Label(models.Model):
    name = models.CharField(_('Name'), max_length=100,
                            blank=False, null=False, unique=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name == '':
            raise ValueError("Label name cannot be empty string")
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
