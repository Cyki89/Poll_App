from rest_framework import status
import pytest


TEST_USER = {
    "first_name": "test",
    "last_name": "test",
    "username": "test",
    "password": "test",
    "email": "test@test.com",
    "groups": []
}


@pytest.fixture
def create_user(api_client):
    def do_create_user(user):
        return api_client.post('/ad/users/', user)
    return do_create_user


@pytest.fixture
def auth_user(api_client):
    def do_auth_user(user):
        return api_client.post('/ad/auth/', user)
    return do_auth_user


@pytest.mark.django_db
class TestAuthenticationAdUser:
    def test_if_invalid_username_returns_400(self, create_user, auth_user):
        user = create_user(TEST_USER)

        response = auth_user({
            "username": TEST_USER['username'] + 'invalid',
            "password": TEST_USER['password'],
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_invalid_password_returns_400(self, create_user, auth_user):
        user = create_user(TEST_USER)

        response = auth_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'] + 'invalid',
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_valid_credentials_returns_200(self, create_user, auth_user):
        user = create_user(TEST_USER)

        response = auth_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })
        
        assert response.status_code == status.HTTP_200_OK
