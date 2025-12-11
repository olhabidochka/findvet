from rest_framework import serializers
from appointments.models import Appointment
from doctors.serializers import DoctorListSerializer
from services.serializers import ServiceSerializer


class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = DoctorListSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'service', 'appointment_date', 'appointment_time',
                  'status', 'status_display', 'notes', 'created_at']


class AppointmentDetailSerializer(serializers.ModelSerializer):
    doctor = DoctorListSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'user_name', 'doctor', 'service', 'appointment_date',
                  'appointment_time', 'status', 'status_display', 'notes',
                  'google_calendar_event_id', 'is_past', 'created_at', 'updated_at']


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'appointment_date', 'appointment_time', 'notes']

    def validate(self, data):
        # Check if appointment slot is available
        existing = Appointment.objects.filter(
            doctor=data['doctor'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            status__in=['pending', 'confirmed']
        ).exists()

        if existing:
            raise serializers.ValidationError("Цей час вже зайнятий.")

        return data


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'status', 'notes']