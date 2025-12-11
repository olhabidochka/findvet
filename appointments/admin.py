from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'appointment_date', 'appointment_time', 'status', 'created_at']
    list_filter = ['status', 'appointment_date', 'created_at']
    search_fields = ['user__username', 'doctor__first_name', 'doctor__last_name']
    actions = ['confirm_appointments', 'cancel_appointments']

    def confirm_appointments(self, request, queryset):
        queryset.update(status='confirmed')

    confirm_appointments.short_description = "Підтвердити вибрані записи"

    def cancel_appointments(self, request, queryset):
        queryset.update(status='cancelled')

    cancel_appointments.short_description = "Скасувати вибрані записи"
