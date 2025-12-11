from django.contrib import admin
from .models import Clinic, ClinicSpecialization

class ClinicSpecializationInline(admin.TabularInline):
    model = ClinicSpecialization
    extra = 1

@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone', 'rating', 'is_active', 'created_at']
    list_filter = ['city', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'address']
    inlines = [ClinicSpecializationInline]
