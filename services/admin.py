from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'clinic', 'service_type', 'price', 'duration_minutes', 'is_available']
    list_filter = ['service_type', 'clinic', 'is_available']
    search_fields = ['name', 'description']
