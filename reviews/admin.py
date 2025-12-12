from django.contrib import admin
from .models import ClinicReview, DoctorReview

@admin.register(ClinicReview)
class ClinicReviewAdmin(admin.ModelAdmin):
    list_display = ['clinic', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['clinic__name', 'user__username', 'comment']

@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['doctor__full_name', 'user__username', 'comment']
