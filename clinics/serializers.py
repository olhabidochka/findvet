from rest_framework import serializers
from .models import Clinic, ClinicSpecialization


class ClinicSpecializationSerializer(serializers.ModelSerializer):
    specialization_display = serializers.CharField(source='get_specialization_display', read_only=True)

    class Meta:
        model = ClinicSpecialization
        fields = ['id', 'specialization', 'specialization_display']


class ClinicListSerializer(serializers.ModelSerializer):
    specializations = ClinicSpecializationSerializer(many=True, read_only=True)

    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address', 'city', 'phone', 'rating', 'image',
                  'specializations', 'latitude', 'longitude']


class ClinicDetailSerializer(serializers.ModelSerializer):
    specializations = ClinicSpecializationSerializer(many=True, read_only=True)

    class Meta:
        model = Clinic
        fields = ['id', 'name', 'description', 'address', 'city', 'phone', 'email',
                  'website', 'latitude', 'longitude', 'working_hours_start',
                  'working_hours_end', 'working_days', 'rating', 'image',
                  'specializations', 'is_active', 'created_at']


class ClinicCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['name', 'description', 'address', 'city', 'phone', 'email',
                  'website', 'latitude', 'longitude', 'working_hours_start',
                  'working_hours_end', 'working_days', 'image', 'is_active']