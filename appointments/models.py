from django.db import models
from django.utils import timezone
from users.models import User
from doctors.models import Doctor
from services.models import Service


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Очікується'),
        ('confirmed', 'Підтверджено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', verbose_name='Користувач')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name='Лікар')
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, related_name='appointments',
                                verbose_name='Послуга')

    appointment_date = models.DateField(verbose_name='Дата прийому')
    appointment_time = models.TimeField(verbose_name='Час прийому')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    notes = models.TextField(blank=True, verbose_name='Примітки')

    google_calendar_event_id = models.CharField(max_length=255, blank=True, null=True,
                                                verbose_name='ID події в Google Calendar')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.full_name} ({self.appointment_date} {self.appointment_time})"

    @property
    def is_past(self):
        appointment_datetime = timezone.make_aware(
            timezone.datetime.combine(self.appointment_date, self.appointment_time)
        )
        return appointment_datetime < timezone.now()

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
