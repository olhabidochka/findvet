from django.db import models
from django.contrib.auth import get_user_model
from clinics.models import Clinic
from doctors.models import Doctor

User = get_user_model()

class ClinicReview(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('clinic', 'user')  # One review per user per clinic
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name} - {self.rating}★"


class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('doctor', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.doctor.full_name} - {self.rating}★"