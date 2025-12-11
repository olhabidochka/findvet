from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import (AppointmentListSerializer, AppointmentDetailSerializer,
                          AppointmentCreateSerializer, AppointmentUpdateSerializer)
from .google_calendar import GoogleCalendarService


class AppointmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'doctor', 'appointment_date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        elif user.role == 'doctor':
            return Appointment.objects.filter(doctor__user=user)
        else:
            return Appointment.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return AppointmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AppointmentUpdateSerializer
        elif self.action == 'list':
            return AppointmentListSerializer
        return AppointmentDetailSerializer

    def perform_create(self, serializer):
        appointment = serializer.save(user=self.request.user)

        # Try to create Google Calendar event
        try:
            calendar_service = GoogleCalendarService()
            event_id = calendar_service.create_appointment_event(appointment)
            if event_id:
                appointment.google_calendar_event_id = event_id
                appointment.save()
        except Exception as e:
            print(f"Could not create calendar event: {e}")

    def perform_update(self, serializer):
        appointment = serializer.save()

        # Try to update Google Calendar event
        if appointment.google_calendar_event_id:
            try:
                calendar_service = GoogleCalendarService()
                calendar_service.update_appointment_event(
                    appointment.google_calendar_event_id,
                    appointment
                )
            except Exception as e:
                print(f"Could not update calendar event: {e}")

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()

        if appointment.status == 'cancelled':
            return Response(
                {'detail': 'Цей запис вже скасовано.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        appointment.status = 'cancelled'
        appointment.save()

        # Try to delete Google Calendar event
        if appointment.google_calendar_event_id:
            try:
                calendar_service = GoogleCalendarService()
                calendar_service.delete_appointment_event(
                    appointment.google_calendar_event_id
                )
            except Exception as e:
                print(f"Could not delete calendar event: {e}")

        return Response(
            {'detail': 'Запис успішно скасовано.'},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        appointment = self.get_object()

        # Only doctors or admins can confirm
        if request.user.role not in ['doctor', 'admin']:
            return Response(
                {'detail': 'Недостатньо прав.'},
                status=status.HTTP_403_FORBIDDEN
            )

        appointment.status = 'confirmed'
        appointment.save()

        return Response(
            {'detail': 'Запис підтверджено.'},
            status=status.HTTP_200_OK
        )
