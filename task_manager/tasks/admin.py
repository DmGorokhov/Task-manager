from django.contrib import admin
from .models import Task


# Register your models here.
@admin.register(Task)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'status', 'executor',
                    'created_at', 'updated_at']
    search_fields = ['name', 'description', 'status', 'executor',
                     'created_at', 'updated_at']
