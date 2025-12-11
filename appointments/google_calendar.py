import datetime
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google Calendar API"""
        token_path = os.path.join(settings.BASE_DIR, 'token.json')
        credentials_path = settings.GOOGLE_CALENDAR_CREDENTIALS

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if os.path.exists(credentials_path):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        credentials_path, SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)
                else:
                    return None

            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())

        if self.creds:
            self.service = build('calendar', 'v3', credentials=self.creds)

    def create_appointment_event(self, appointment):
        """Create a calendar event for an appointment"""
        if not self.service:
            return None

        try:
            start_datetime = datetime.datetime.combine(
                appointment.appointment_date,
                appointment.appointment_time
            )

            # Assume 30 minutes duration if service duration not available
            duration = appointment.service.duration_minutes if appointment.service else 30
            end_datetime = start_datetime + datetime.timedelta(minutes=duration)

            event = {
                'summary': f'Прийом у {appointment.doctor.full_name}',
                'location': appointment.doctor.clinic.address,
                'description': f'Послуга: {appointment.service.name if appointment.service else "Консультація"}\n'
                               f'Лікар: {appointment.doctor.full_name}\n'
                               f'Клініка: {appointment.doctor.clinic.name}\n'
                               f'Примітки: {appointment.notes}',
                'start': {
                    'dateTime': start_datetime.isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
                'end': {
                    'dateTime': end_datetime.isoformat(),
                    'timeZone': 'Europe/Kiev',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                    ],
                },
            }

            created_event = self.service.events().insert(
                calendarId='primary',
                body=event
            ).execute()

            return created_event.get('id')

        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def update_appointment_event(self, event_id, appointment):
        """Update existing calendar event"""
        if not self.service or not event_id:
            return False

        try:
            start_datetime = datetime.datetime.combine(
                appointment.appointment_date,
                appointment.appointment_time
            )

            duration = appointment.service.duration_minutes if appointment.service else 30
            end_datetime = start_datetime + datetime.timedelta(minutes=duration)

            event = self.service.events().get(
                calendarId='primary',
                eventId=event_id
            ).execute()

            event['start'] = {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Kiev',
            }
            event['end'] = {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Europe/Kiev',
            }
            event['description'] = f'Послуга: {appointment.service.name if appointment.service else "Консультація"}\n' \
                                   f'Лікар: {appointment.doctor.full_name}\n' \
                                   f'Клініка: {appointment.doctor.clinic.name}\n' \
                                   f'Примітки: {appointment.notes}'

            updated_event = self.service.events().update(
                calendarId='primary',
                eventId=event_id,
                body=event
            ).execute()

            return True

        except HttpError as error:
            print(f'An error occurred: {error}')
            return False

    def delete_appointment_event(self, event_id):
        """Delete calendar event"""
        if not self.service or not event_id:
            return False

        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True

        except HttpError as error:
            print(f'An error occurred: {error}')
            return False