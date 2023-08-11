from django.contrib import admin
from .models import Status


# Register your models here.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ['name', 'created_at', 'updated_at']
