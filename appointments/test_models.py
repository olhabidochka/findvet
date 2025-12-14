import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from clinics.models import Clinic
from doctors.models import Doctor
from services.models import Service
from appointments.models import Appointment

User = get_user_model()


@pytest.mark.django_db
@pytest.mark.unit
class TestAppointmentModel:


    def test_create_appointment(self, db):

        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

        clinic = Clinic.objects.create(
            name='Test Clinic',
            address='Test St 1',
            city='Kyiv',
            phone='+380501234567',
            email='clinic@test.com',
            latitude=50.45,
            longitude=30.52,
            working_hours_start='09:00',
            working_hours_end='18:00'
        )

        doctor_user = User.objects.create_user(
            username='doctor',
            email='doctor@test.com',
            password='pass',
            role='doctor'
        )

        doctor = Doctor.objects.create(
            user=doctor_user,
            clinic=clinic,
            first_name='John',
            last_name='Doe',
            specialization='general',
            experience_years=5,
            education='University',
            bio='Bio',
            phone='+380507654321',
            email='doctor@test.com'
        )

        service = Service.objects.create(
            clinic=clinic,
            name='Consultation',
            service_type='consultation',
            description='Test',
            price=500.00,
            duration_minutes=30
        )

        tomorrow = (timezone.now() + timedelta(days=1)).date()

        appointment = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='14:00',
            status='pending'
        )

        assert appointment.id is not None
        assert appointment.user == user
        assert appointment.doctor == doctor
        assert appointment.service == service
        assert appointment.status == 'pending'
        assert str(appointment) == f"{user.username} -> {doctor.full_name} ({tomorrow} 14:00)"

    def test_appointment_default_status(self, db):

        user = User.objects.create_user(username='user1', password='pass')
        clinic = Clinic.objects.create(
            name='Clinic',
            address='Addr',
            city='City',
            phone='+380501111111',
            email='c@test.com',
            latitude=50.0,
            longitude=30.0,
            working_hours_start='09:00',
            working_hours_end='18:00'
        )
        doctor_user = User.objects.create_user(username='doc', password='pass', role='doctor')
        doctor = Doctor.objects.create(
            user=doctor_user,
            clinic=clinic,
            first_name='Dr',
            last_name='Test',
            specialization='general',
            experience_years=3,
            education='Uni',
            bio='B',
            phone='+380502222222',
            email='d@test.com'
        )
        service = Service.objects.create(
            clinic=clinic,
            name='Service',
            service_type='consultation',
            description='D',
            price=100,
            duration_minutes=30
        )

        appointment = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=(timezone.now() + timedelta(days=1)).date(),
            appointment_time='10:00'
        )

        assert appointment.status == 'pending'

    def test_appointment_is_past_property(self, db):

        user = User.objects.create_user(username='user2', password='pass')
        clinic = Clinic.objects.create(
            name='Clinic',
            address='Addr',
            city='City',
            phone='+380501111111',
            email='c@test.com',
            latitude=50.0,
            longitude=30.0,
            working_hours_start='09:00',
            working_hours_end='18:00'
        )
        doctor_user = User.objects.create_user(username='doc2', password='pass', role='doctor')
        doctor = Doctor.objects.create(
            user=doctor_user,
            clinic=clinic,
            first_name='Dr',
            last_name='Test',
            specialization='general',
            experience_years=3,
            education='Uni',
            bio='B',
            phone='+380502222222',
            email='d@test.com'
        )
        service = Service.objects.create(
            clinic=clinic,
            name='Service',
            service_type='consultation',
            description='D',
            price=100,
            duration_minutes=30
        )


        yesterday = (timezone.now() - timedelta(days=1)).date()
        past_appointment = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=yesterday,
            appointment_time='10:00'
        )


        tomorrow = (timezone.now() + timedelta(days=1)).date()
        future_appointment = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='10:00'
        )

        assert past_appointment.is_past is True
        assert future_appointment.is_past is False

    def test_appointment_unique_constraint(self, db):

        user1 = User.objects.create_user(username='user3', password='pass')
        user2 = User.objects.create_user(username='user4', password='pass')

        clinic = Clinic.objects.create(
            name='Clinic',
            address='Addr',
            city='City',
            phone='+380501111111',
            email='c@test.com',
            latitude=50.0,
            longitude=30.0,
            working_hours_start='09:00',
            working_hours_end='18:00'
        )
        doctor_user = User.objects.create_user(username='doc3', password='pass', role='doctor')
        doctor = Doctor.objects.create(
            user=doctor_user,
            clinic=clinic,
            first_name='Dr',
            last_name='Test',
            specialization='general',
            experience_years=3,
            education='Uni',
            bio='B',
            phone='+380502222222',
            email='d@test.com'
        )
        service = Service.objects.create(
            clinic=clinic,
            name='Service',
            service_type='consultation',
            description='D',
            price=100,
            duration_minutes=30
        )

        tomorrow = (timezone.now() + timedelta(days=1)).date()


        Appointment.objects.create(
            user=user1,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='15:00',
            status='pending'
        )


        with pytest.raises(IntegrityError):
            Appointment.objects.create(
                user=user2,
                doctor=doctor,
                service=service,
                appointment_date=tomorrow,
                appointment_time='15:00',
                status='pending'
            )

    def test_appointment_ordering(self, db):

        user = User.objects.create_user(username='user5', password='pass')
        clinic = Clinic.objects.create(
            name='Clinic',
            address='Addr',
            city='City',
            phone='+380501111111',
            email='c@test.com',
            latitude=50.0,
            longitude=30.0,
            working_hours_start='09:00',
            working_hours_end='18:00'
        )
        doctor_user = User.objects.create_user(username='doc4', password='pass', role='doctor')
        doctor = Doctor.objects.create(
            user=doctor_user,
            clinic=clinic,
            first_name='Dr',
            last_name='Test',
            specialization='general',
            experience_years=3,
            education='Uni',
            bio='B',
            phone='+380502222222',
            email='d@test.com'
        )
        service = Service.objects.create(
            clinic=clinic,
            name='Service',
            service_type='consultation',
            description='D',
            price=100,
            duration_minutes=30
        )

        tomorrow = (timezone.now() + timedelta(days=1)).date()
        day_after = (timezone.now() + timedelta(days=2)).date()


        apt2 = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=day_after,
            appointment_time='10:00'
        )
        apt1 = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='14:00'
        )
        apt3 = Appointment.objects.create(
            user=user,
            doctor=doctor,
            service=service,
            appointment_date=day_after,
            appointment_time='15:00'
        )


        appointments = list(Appointment.objects.all())


        assert appointments[0] == apt3
        assert appointments[1] == apt2
        assert appointments[2] == apt1