from rest_framework import serializers
from services.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'clinic', 'clinic_name', 'name', 'service_type',
                  'service_type_display', 'description', 'price',
                  'duration_minutes', 'is_available', 'created_at']