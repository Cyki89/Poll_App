import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(username, is_staff=False):
        user = User.objects.get(username=username)
        if is_staff:
            user.is_staff = True
            user.save()
        return api_client.force_authenticate(user=user)
    return do_authenticate