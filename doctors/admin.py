from django.contrib import admin
from .models import Doctor, DoctorSchedule, FavoriteDoctor

class DoctorScheduleInline(admin.TabularInline):
    model = DoctorSchedule
    extra = 1

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'clinic', 'experience_years', 'rating', 'is_available']
    list_filter = ['specialization', 'clinic', 'is_available']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [DoctorScheduleInline]

@admin.register(FavoriteDoctor)
class FavoriteDoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'created_at']
    list_filter = ['created_at']
