from rest_framework import status
from ad_service.models import ADGroup, ADUser
import pytest
from model_bakery import baker


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
def retrive_user(api_client):
    def do_retrieve_user(id):
        return api_client.get(f'/ad/users/{id}/')
    return do_retrieve_user


@pytest.fixture
def retrive_user_list(api_client):
    def do_retrive_user_list():
        return api_client.get(f'/ad/users/')
    return do_retrive_user_list


@pytest.mark.django_db
class TestCreateAdGroup:
    def test_if_invalid_data_returns_400(self, create_user):
        test_user = TEST_USER.copy()
        del test_user['username']
        
        response = create_user(test_user)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] is not None

    def test_if_not_unique_username_returns_400(self, create_user):
        create_user(TEST_USER)
        
        response = create_user(TEST_USER)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['username'] is not None

    def test_if_valid_data_returns_201(self, create_user):
        groups = baker.make(ADGroup, 2)
        test_user = TEST_USER.copy()
        test_user['groups'] = [group.id for group in groups]
        
        response = create_user(test_user)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['groups'] == test_user['groups']


@pytest.mark.django_db
class TestRetrieveAdUser:
    def test_if_user_not_exists_return_404(self, retrive_user):
        response = retrive_user(0)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_user_exists_return_200(self, retrive_user):
        user = baker.make(ADUser)

        response = retrive_user(user.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == user.id
        assert response.data['username'] == user.username

@pytest.mark.django_db
class TestRetrieveAduserList:
    def test_if_user_list_is_empty(self, retrive_user_list):
        response = retrive_user_list()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_if_user_list_is_not_empty(self, retrive_user_list):
        users = baker.make(ADUser, 2)
        
        response = retrive_user_list()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2