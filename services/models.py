from django.db import models
from django.core.validators import MinValueValidator
from clinics.models import Clinic


class Service(models.Model):
    SERVICE_TYPE_CHOICES = (
        ('consultation', 'Консультація'),
        ('vaccination', 'Вакцинація'),
        ('surgery', 'Хірургія'),
        ('dental', 'Стоматологія'),
        ('grooming', 'Догляд'),
        ('lab_test', 'Лабораторні тести'),
        ('xray', 'Рентген'),
        ('ultrasound', 'УЗД'),
        ('therapy', 'Терапія'),
        ('emergency', 'Екстрена допомога'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200, verbose_name='Назва послуги')
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, verbose_name='Тип послуги')
    description = models.TextField(verbose_name='Опис')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Ціна (грн)'
    )
    duration_minutes = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=30,
        verbose_name='Тривалість (хв)'
    )
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.clinic.name}"

    class Meta:
        ordering = ['service_type', 'name']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'