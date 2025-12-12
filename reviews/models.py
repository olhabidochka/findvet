from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from clinics.models import Clinic
from doctors.models import Doctor


class ClinicReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_reviews')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оцінка'
    )
    comment = models.TextField(verbose_name='Коментар')
    is_approved = models.BooleanField(default=False, verbose_name='Схвалено')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.clinic.name} ({self.rating}/5)"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'clinic']
        verbose_name = 'Відгук про клініку'
        verbose_name_plural = 'Відгуки про клініки'


class DoctorReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_reviews')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Оцінка'
    )
    comment = models.TextField(verbose_name='Коментар')
    is_approved = models.BooleanField(default=False, verbose_name='Схвалено')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.full_name} ({self.rating}/5)"

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'doctor']
        verbose_name = 'Відгук про лікаря'
        verbose_name_plural = 'Відгуки про лікарів'