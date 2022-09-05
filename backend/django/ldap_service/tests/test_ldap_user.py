from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
import jwt
import pytest


TEST_USER = {
    "first_name": "test",
    "last_name": "test",
    "username": "test",
    "password": "test",
    "email": "test@test.com",
    "groups": [],
    "is_active": True
}


USER_TO_UPDATE = {
    "first_name": "test2",
    "last_name": "test2",
    "username": "test",
    "password": "test2",
    "email": "test2@test2.com",
    "is_active": True
}


@pytest.fixture
def create_ad_user(api_client):
    def do_create_user(user):
        return api_client.post('/ad/users/', user)
    return do_create_user


@pytest.fixture
def auth_ldap_user(api_client):
    def do_auth_user(user):
        return api_client.post('/ldap/jwt/create/', user)
    return do_auth_user


@pytest.fixture
def refresh_token(api_client):
    def do_refresh_token():
        return api_client.post('/ldap/jwt/refresh/')
    return do_refresh_token


@pytest.fixture
def logout(api_client):
    def do_logout():
        return api_client.post('/ldap/logout/')
    return do_logout


@pytest.mark.django_db
class TestLdapUserLogin:
    def test_if_invalid_credentails_returns_400(self, auth_ldap_user, create_ad_user):
        ad_user = create_ad_user(TEST_USER)

        response = auth_ldap_user({
            "username": TEST_USER['username'] + 'invalid',
            "password": TEST_USER['password'],
        })
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_valid_credentails_returns_200(self, auth_ldap_user, create_ad_user):
        ad_user = create_ad_user(TEST_USER)
        
        response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data 
        assert 'refresh_token' in response.client.cookies

        payload = jwt.decode(response.data['access'], settings.SECRET_KEY, algorithms=["HS256"])
        assert payload['username'] == TEST_USER['username']

    def test_create_user_object_if_not_exists(self, auth_ldap_user, create_ad_user):
        ad_user = create_ad_user(TEST_USER)

        response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })
        user = User.objects.filter(username=TEST_USER['username']).first()
        
        assert response.status_code == status.HTTP_200_OK
        assert TEST_USER['first_name'] == user.first_name
        assert TEST_USER['last_name'] == user.last_name
        assert 'access' in response.data
        assert 'refresh_token' in response.client.cookies

        payload = jwt.decode(response.data['access'], settings.SECRET_KEY, algorithms=["HS256"])
        assert payload['username'] == TEST_USER['username']

    def test_update_user_object_if_exists(self, auth_ldap_user, create_ad_user):
        User.objects.create(**USER_TO_UPDATE)
        create_ad_user(TEST_USER)

        response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })    
        
        updated_user = User.objects.filter(username=TEST_USER['username']).first()
        
        assert response.status_code == status.HTTP_200_OK
        assert TEST_USER['first_name'] == updated_user.first_name
        assert TEST_USER['last_name'] == updated_user.last_name
        assert 'access' in response.data
        assert 'refresh_token' in response.client.cookies 

        payload = jwt.decode(response.data['access'], settings.SECRET_KEY, algorithms=["HS256"])
        assert payload['username'] == TEST_USER['username']


@pytest.mark.django_db
class TestRefreshToken:
    def test_if_valid_credentials_return_201(self, auth_ldap_user, create_ad_user, refresh_token):
        ad_user = create_ad_user(TEST_USER)

        auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        response = refresh_token()
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data 
        assert 'refresh_token' in response.client.cookies

        payload = jwt.decode(response.data['access'], settings.SECRET_KEY, algorithms=["HS256"])
        assert payload['username'] == TEST_USER['username']

    def test_if_no_cookie_return_401(self, refresh_token):
        response = refresh_token()
        assert not 'refresh_token' in response.client.cookies
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestLdapUserLogout:
    def test_if_successfull_logout_return_403(self, create_ad_user, auth_ldap_user, logout):
        ad_user = create_ad_user(TEST_USER)

        response_login = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })
        print(response_login.client.cookies['refresh_token'].items())

        assert 'refresh_token' in response_login.client.cookies
        
        response_logout = logout()
        assert response_logout.status_code == status.HTTP_204_NO_CONTENT
        assert response_logout.client.cookies['refresh_token']['max-age'] == 0


