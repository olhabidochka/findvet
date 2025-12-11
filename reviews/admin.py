from django.contrib import admin
from .models import ClinicReview, DoctorReview


@admin.register(ClinicReview)
class ClinicReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'clinic', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['user__username', 'clinic__name', 'comment']
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Схвалити вибрані відгуки"


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['user__username', 'doctor__first_name', 'doctor__last_name', 'comment']
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    approve_reviews.short_description = "Схвалити вибрані відгуки"
