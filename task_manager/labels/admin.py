from django.contrib import admin
from .models import Label


# Register your models here.
@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ['name', 'created_at']
