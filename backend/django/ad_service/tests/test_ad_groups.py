from rest_framework import status
from ad_service.models import ADGroup
import pytest
from model_bakery import baker


TEST_AD_GROUP1 = {
    'name': 'ad_group1',
    'is_active': True
}


TEST_AD_GROUP2 = {
    'name': 'ad_group2',
    'is_active': True
}


@pytest.fixture
def create_group(api_client):
    def do_create_group(group):
        return api_client.post('/ad/groups/', group)
    return do_create_group


@pytest.fixture
def retrive_group(api_client):
    def do_retrieve_group(id):
        return api_client.get(f'/ad/groups/{id}/')
    return do_retrieve_group


@pytest.fixture
def retrive_group_list(api_client):
    def do_retrive_group_list():
        return api_client.get(f'/ad/groups/')
    return do_retrive_group_list


@pytest.mark.django_db
class TestCreateAdGroup:
    def test_if_invalid_data_returns_400(self, create_group):
        response = create_group({})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_not_unique_name_returns_400(self, create_group):
        create_group(TEST_AD_GROUP1)
        response = create_group(TEST_AD_GROUP1)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None

    def test_if_valid_data_returns_201(self, create_group):
        response = create_group(TEST_AD_GROUP1)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveAdGroup:
    def test_if_group_not_exists_return_404(self, retrive_group):
        response = retrive_group(0)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_group_exists_return_200(self, retrive_group):
        group = baker.make(ADGroup)

        response = retrive_group(group.id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == group.id
        assert response.data['name'] == group.name


@pytest.mark.django_db
class TestRetrieveAdGroupList:
    def test_if_group_list_is_empty(self, retrive_group_list):
        response = retrive_group_list()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0

    def test_if_group_list_is_not_empty(self, retrive_group_list):
        groups = baker.make(ADGroup, 2)
        
        response = retrive_group_list()

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2
