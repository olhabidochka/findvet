from django.db import models
from django.utils import timezone
from datetime import datetime, time as dt_time
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

        if isinstance(self.appointment_time, dt_time):
            time_str = self.appointment_time.strftime('%H:%M:%S')
        else:
            time_str = str(self.appointment_time)
        return f"{self.user.username} -> {self.doctor.full_name} ({self.appointment_date} {time_str})"

    @property
    def is_past(self):

        if isinstance(self.appointment_time, str):

            try:
                time_obj = datetime.strptime(self.appointment_time, '%H:%M:%S').time()
            except ValueError:
                time_obj = datetime.strptime(self.appointment_time, '%H:%M').time()
        else:
            time_obj = self.appointment_time


        appointment_datetime = datetime.combine(self.appointment_date, time_obj)


        if timezone.is_naive(appointment_datetime):
            appointment_datetime = timezone.make_aware(appointment_datetime)

        return appointment_datetime < timezone.now()

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Запис'
        verbose_name_plural = 'Записи'
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
