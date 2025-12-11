from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Clinic(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва клініки')
    description = models.TextField(verbose_name='Опис')
    address = models.CharField(max_length=300, verbose_name='Адреса')
    city = models.CharField(max_length=100, verbose_name='Місто')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Веб-сайт')

    # Геолокація
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Довгота')

    # Години роботи
    working_hours_start = models.TimeField(verbose_name='Початок роботи')
    working_hours_end = models.TimeField(verbose_name='Кінець роботи')
    working_days = models.CharField(max_length=100, default='Пн-Пт', verbose_name='Робочі дні')

    # Рейтинг
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Рейтинг'
    )

    image = models.ImageField(upload_to='clinics/', blank=True, null=True, verbose_name='Фото')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rating', 'name']
        verbose_name = 'Клініка'
        verbose_name_plural = 'Клініки'


class ClinicSpecialization(models.Model):
    SPECIALIZATION_CHOICES = (
        ('therapy', 'Терапія'),
        ('surgery', 'Хірургія'),
        ('vaccination', 'Вакцинація'),
        ('dental', 'Стоматологія'),
        ('grooming', 'Догляд за тваринами'),
        ('lab', 'Лабораторні дослідження'),
        ('emergency', 'Екстрена допомога'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='specializations')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)

    def __str__(self):
        return f"{self.clinic.name} - {self.get_specialization_display()}"

    class Meta:
        unique_together = ['clinic', 'specialization']
        verbose_name = 'Спеціалізація клініки'
        verbose_name_plural = 'Спеціалізації клінік'
