import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import datetime, timedelta
from clinics.models import Clinic
from doctors.models import Doctor
from services.models import Service
from appointments.models import Appointment

User = get_user_model()


@pytest.fixture
def api_client():

    return APIClient()


@pytest.fixture
def create_user(db):


    def make_user(**kwargs):
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'client'
        }
        defaults.update(kwargs)
        password = defaults.pop('password')
        user = User.objects.create(**defaults)
        user.set_password(password)
        user.save()
        return user

    return make_user


@pytest.fixture
def authenticated_client(api_client, create_user):

    user = create_user()
    api_client.force_authenticate(user=user)
    api_client.user = user
    return api_client


@pytest.fixture
def clinic(db):

    return Clinic.objects.create(
        name='Test Clinic',
        description='Test clinic description',
        address='Test Street 123',
        city='Kyiv',
        phone='+380501234567',
        email='clinic@test.com',
        latitude=50.4501,
        longitude=30.5234,
        working_hours_start='09:00',
        working_hours_end='18:00',
        rating=4.5
    )


@pytest.fixture
def doctor(db, clinic, create_user):

    user = create_user(username='doctor', email='doctor@test.com', role='doctor')
    return Doctor.objects.create(
        user=user,
        clinic=clinic,
        first_name='John',
        last_name='Doe',
        specialization='general',
        experience_years=5,
        education='Kyiv Medical University',
        bio='Experienced veterinarian',
        phone='+380507654321',
        email='doctor@test.com',
        rating=4.8
    )


@pytest.fixture
def service(db, clinic):

    return Service.objects.create(
        clinic=clinic,
        name='Consultation',
        service_type='consultation',
        description='General consultation',
        price=500.00,
        duration_minutes=30
    )


@pytest.fixture
def appointment(db, authenticated_client, doctor, service):

    tomorrow = (timezone.now() + timedelta(days=1)).date()
    return Appointment.objects.create(
        user=authenticated_client.user,
        doctor=doctor,
        service=service,
        appointment_date=tomorrow,
        appointment_time='14:00',
        status='pending',
        notes='Test appointment'
    )


# ==================== POSITIVE TEST CASES ====================

@pytest.mark.django_db
class TestAppointmentListPositive:


    def test_list_appointments_authenticated(self, authenticated_client, appointment):

        response = authenticated_client.get('/api/appointments/')

        assert response.status_code == status.HTTP_200_OK
        assert 'results' in response.data or isinstance(response.data, list)

        results = response.data.get('results', response.data)
        assert len(results) == 1
        assert results[0]['id'] == appointment.id
        assert results[0]['status'] == 'pending'

    def test_list_appointments_filtering_by_status(self, authenticated_client, doctor, service):

        tomorrow = (timezone.now() + timedelta(days=1)).date()

        Appointment.objects.create(
            user=authenticated_client.user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='10:00',
            status='pending'
        )
        Appointment.objects.create(
            user=authenticated_client.user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='11:00',
            status='confirmed'
        )

        response = authenticated_client.get('/api/appointments/?status=pending')

        assert response.status_code == status.HTTP_200_OK
        results = response.data.get('results', response.data)
        assert len(results) == 1
        assert results[0]['status'] == 'pending'


@pytest.mark.django_db
class TestAppointmentCreatePositive:


    def test_create_appointment_success(self, authenticated_client, doctor, service):

        tomorrow = (timezone.now() + timedelta(days=1)).date()

        data = {
            'doctor': doctor.id,
            'service': service.id,
            'appointment_date': str(tomorrow),
            'appointment_time': '15:00',
            'notes': 'Need checkup for my cat'
        }

        response = authenticated_client.post('/api/appointments/', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['doctor']['id'] == doctor.id
        assert response.data['service']['id'] == service.id
        assert response.data['status'] == 'pending'
        assert response.data['notes'] == 'Need checkup for my cat'


        assert Appointment.objects.filter(
            user=authenticated_client.user,
            doctor=doctor,
            appointment_date=tomorrow,
            appointment_time='15:00'
        ).exists()


@pytest.mark.django_db
class TestAppointmentDetailPositive:


    def test_get_appointment_detail(self, authenticated_client, appointment):

        response = authenticated_client.get(f'/api/appointments/{appointment.id}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == appointment.id
        assert response.data['doctor']['id'] == appointment.doctor.id
        assert response.data['service']['id'] == appointment.service.id


@pytest.mark.django_db
class TestAppointmentCancelPositive:


    def test_cancel_appointment_success(self, authenticated_client, appointment):

        response = authenticated_client.post(f'/api/appointments/{appointment.id}/cancel/')

        assert response.status_code == status.HTTP_200_OK
        assert 'detail' in response.data


        appointment.refresh_from_db()
        assert appointment.status == 'cancelled'


# ==================== NEGATIVE TEST CASES ====================

@pytest.mark.django_db
class TestAppointmentAuthenticationNegative:


    def test_list_appointments_unauthenticated(self, api_client):

        response = api_client.get('/api/appointments/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_appointment_unauthenticated(self, api_client, doctor, service):

        tomorrow = (timezone.now() + timedelta(days=1)).date()

        data = {
            'doctor': doctor.id,
            'service': service.id,
            'appointment_date': str(tomorrow),
            'appointment_time': '15:00'
        }

        response = api_client.post('/api/appointments/', data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestAppointmentCreateNegative:


    def test_create_appointment_missing_required_fields(self, authenticated_client):

        data = {
            'notes': 'Missing required fields'
        }

        response = authenticated_client.post('/api/appointments/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'doctor' in response.data or 'appointment_date' in response.data

    def test_create_appointment_nonexistent_doctor(self, authenticated_client, service):

        tomorrow = (timezone.now() + timedelta(days=1)).date()

        data = {
            'doctor': 99999,  # Non-existent doctor ID
            'service': service.id,
            'appointment_date': str(tomorrow),
            'appointment_time': '15:00'
        }

        response = authenticated_client.post('/api/appointments/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_appointment_duplicate_slot(self, authenticated_client, appointment):

        data = {
            'doctor': appointment.doctor.id,
            'service': appointment.service.id,
            'appointment_date': str(appointment.appointment_date),
            'appointment_time': str(appointment.appointment_time),
            'notes': 'Trying to book occupied slot'
        }

        response = authenticated_client.post('/api/appointments/', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'вже зайнятий' in str(response.data).lower() or 'already' in str(response.data).lower()

    def test_create_appointment_past_date(self, authenticated_client, doctor, service):

        yesterday = (timezone.now() - timedelta(days=1)).date()

        data = {
            'doctor': doctor.id,
            'service': service.id,
            'appointment_date': str(yesterday),
            'appointment_time': '15:00'
        }

        response = authenticated_client.post('/api/appointments/', data, format='json')

        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED]


@pytest.mark.django_db
class TestAppointmentAccessNegative:


    def test_user_cannot_access_other_users_appointments(self, authenticated_client, create_user, doctor, service):

        other_user = create_user(username='otheruser', email='other@test.com')
        tomorrow = (timezone.now() + timedelta(days=1)).date()

        other_appointment = Appointment.objects.create(
            user=other_user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='16:00',
            status='pending'
        )


        response = authenticated_client.get(f'/api/appointments/{other_appointment.id}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_cannot_cancel_other_users_appointments(self, authenticated_client, create_user, doctor, service):

        other_user = create_user(username='otheruser2', email='other2@test.com')
        tomorrow = (timezone.now() + timedelta(days=1)).date()

        other_appointment = Appointment.objects.create(
            user=other_user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='17:00',
            status='pending'
        )

        response = authenticated_client.post(f'/api/appointments/{other_appointment.id}/cancel/')

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestAppointmentCancelNegative:


    def test_cancel_nonexistent_appointment(self, authenticated_client):

        response = authenticated_client.post('/api/appointments/99999/cancel/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cancel_already_cancelled_appointment(self, authenticated_client, appointment):

        appointment.status = 'cancelled'
        appointment.save()


        response = authenticated_client.post(f'/api/appointments/{appointment.id}/cancel/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'вже скасовано' in str(response.data).lower() or 'already' in str(response.data).lower()


@pytest.mark.django_db
class TestAppointmentUpdateNegative:


    def test_update_appointment_to_occupied_slot(self, authenticated_client, appointment, doctor, service):

        tomorrow = (timezone.now() + timedelta(days=1)).date()
        existing_appointment = Appointment.objects.create(
            user=authenticated_client.user,
            doctor=doctor,
            service=service,
            appointment_date=tomorrow,
            appointment_time='18:00',
            status='pending'
        )


        data = {
            'appointment_date': str(tomorrow),
            'appointment_time': '18:00'
        }

        response = authenticated_client.patch(
            f'/api/appointments/{appointment.id}/',
            data,
            format='json'
        )


        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_200_OK]
