from django.forms import ModelForm
from .models import Status


class StatusForm(ModelForm):

    class Meta:
        model = Status
        fields = ['name', ]
