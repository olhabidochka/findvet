import pytest
from django.core.management import call_command


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):

    with django_db_blocker.unblock():
        # You can load fixtures here if needed
        pass


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):

    pass