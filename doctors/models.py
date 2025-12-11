from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from clinics.models import Clinic
from users.models import User


class Doctor(models.Model):
    SPECIALIZATION_CHOICES = (
        ('general', 'Загальна практика'),
        ('surgeon', 'Хірург'),
        ('dentist', 'Стоматолог'),
        ('dermatologist', 'Дерматолог'),
        ('cardiologist', 'Кардіолог'),
        ('ophthalmologist', 'Офтальмолог'),
        ('orthopedist', 'Ортопед'),
        ('neurologist', 'Невролог'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='doctors')

    first_name = models.CharField(max_length=100, verbose_name='Ім\'я')
    last_name = models.CharField(max_length=100, verbose_name='Прізвище')
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, verbose_name='Спеціалізація')
    experience_years = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Досвід (років)')
    education = models.TextField(verbose_name='Освіта')
    bio = models.TextField(verbose_name='Про лікаря')

    photo = models.ImageField(upload_to='doctors/', blank=True, null=True, verbose_name='Фото')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        verbose_name='Рейтинг'
    )

    is_available = models.BooleanField(default=True, verbose_name='Доступний')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Д-р {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['-rating', 'last_name']
        verbose_name = 'Лікар'
        verbose_name_plural = 'Лікарі'


class DoctorSchedule(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Понеділок'),
        (1, 'Вівторок'),
        (2, 'Середа'),
        (3, 'Четвер'),
        (4, 'П\'ятниця'),
        (5, 'Субота'),
        (6, 'Неділя'),
    )

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES, verbose_name='День тижня')
    start_time = models.TimeField(verbose_name='Початок')
    end_time = models.TimeField(verbose_name='Кінець')
    is_active = models.BooleanField(default=True, verbose_name='Активний')

    def __str__(self):
        return f"{self.doctor.full_name} - {self.get_weekday_display()}"

    class Meta:
        unique_together = ['doctor', 'weekday']
        ordering = ['weekday', 'start_time']
        verbose_name = 'Розклад лікаря'
        verbose_name_plural = 'Розклади лікарів'


class FavoriteDoctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_doctors')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.doctor.full_name}"

    class Meta:
        unique_together = ['user', 'doctor']
        verbose_name = 'Обраний лікар'
        verbose_name_plural = 'Обрані лікарі'
