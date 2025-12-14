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

    doctor_detail = DoctorListSerializer(source='doctor', read_only=True)
    service_detail = ServiceSerializer(source='service', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'service', 'appointment_date', 'appointment_time',
                  'notes', 'doctor_detail', 'service_detail', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']

        validators = []

    def validate(self, data):

        existing = Appointment.objects.filter(
            doctor=data['doctor'],
            appointment_date=data['appointment_date'],
            appointment_time=data['appointment_time'],
            status__in=['pending', 'confirmed']
        ).exists()

        if existing:
            raise serializers.ValidationError(
                "Цей час вже зайнятий."
            )

        return data

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        if 'doctor_detail' in representation:
            representation['doctor'] = representation.pop('doctor_detail')

        if 'service_detail' in representation:
            representation['service'] = representation.pop('service_detail')
        return representation


class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time', 'status', 'notes']

    def validate(self, data):

        doctor = self.instance.doctor
        appointment_date = data.get('appointment_date', self.instance.appointment_date)
        appointment_time = data.get('appointment_time', self.instance.appointment_time)


        conflicting = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=['pending', 'confirmed']
        ).exclude(pk=self.instance.pk)

        if conflicting.exists():
            raise serializers.ValidationError(
                "Цей час вже зайнятий."
            )

        return data