from rest_framework import serializers
from .models import Doctor, DoctorSchedule, FavoriteDoctor
from clinics.serializers import ClinicListSerializer


class DoctorScheduleSerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_weekday_display', read_only=True)

    class Meta:
        model = DoctorSchedule
        fields = ['id', 'weekday', 'weekday_display', 'start_time', 'end_time', 'is_active']


class DoctorListSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'full_name', 'specialization',
                  'specialization_display', 'experience_years', 'rating', 'photo',
                  'clinic_name', 'is_available']


class DoctorDetailSerializer(serializers.ModelSerializer):
    clinic = ClinicListSerializer(read_only=True)
    schedules = DoctorScheduleSerializer(many=True, read_only=True)
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'first_name', 'last_name', 'full_name', 'specialization',
                  'specialization_display', 'experience_years', 'education', 'bio',
                  'photo', 'phone', 'email', 'rating', 'clinic', 'schedules',
                  'is_available', 'created_at']


class DoctorCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['clinic', 'first_name', 'last_name', 'specialization',
                  'experience_years', 'education', 'bio', 'photo', 'phone',
                  'email', 'is_available']


class FavoriteDoctorSerializer(serializers.ModelSerializer):
    doctor = DoctorListSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteDoctor
        fields = ['id', 'doctor', 'doctor_id', 'created_at']