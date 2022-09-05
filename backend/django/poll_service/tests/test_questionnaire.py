from urllib import response
from rest_framework import status
from model_bakery import baker
import pytest

from poll_service.models import Questionnaire

ADMINS_GROUP=1

TEST_QUESTIONNAIRE = {
    "name": "test_name",
    "description": "test_desc"
}

TEST_USER = {
    "first_name": "test",
    "last_name": "test",
    "username": "test",
    "password": "test",
    "email": "test@test.com",
    "groups": [],
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
def create_questionnaire(api_client):
    def do_create_questionnaire(questionnaire):
        return api_client.post('/poll/questionnaires/', questionnaire)
    return do_create_questionnaire


@pytest.fixture
def retrieve_questionnaire(api_client):
    def do_retrieve_questionnaire(id):
        return api_client.get(f'/poll/questionnaires/{id}/')
    return do_retrieve_questionnaire


@pytest.fixture
def update_questionnaire(api_client):
    def do_update_questionnaire(id, data):
        return api_client.patch(f'/poll/questionnaires/{id}/', data)
    return do_update_questionnaire


@pytest.fixture
def delete_questionnaires(api_client):
    def do_delete_questionnaires(questionnaires):
        return api_client.post(f'/poll/questionnaires/delete/', {"questionnaires": questionnaires})
    return do_delete_questionnaires


@pytest.fixture
def deactivate_questionnaires(api_client):
    def do_deactivate_questionnaires(questionnaires):
        return api_client.post(f'/poll/questionnaires/deactivate/', {"questionnaires": questionnaires})
    return do_deactivate_questionnaires


@pytest.fixture
def retrieve_questionnaire_list(api_client):
    def do_retrieve_questionnaire_list():
        return api_client.get(f'/poll/questionnaires/')
    return do_retrieve_questionnaire_list


@pytest.mark.django_db
class TestCreateQuestionnaire:
    def test_if_user_not_authenticate_returns_401(self, create_questionnaire):
        response = create_questionnaire({})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_authorizated(self, create_ad_user, auth_ldap_user, authenticate, create_questionnaire):
        response = create_questionnaire({})

        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])
        response = create_questionnaire({})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_return_400(self, create_ad_user, auth_ldap_user, authenticate, create_questionnaire):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        response = create_questionnaire({})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['name'] is not None
    
    def test_if_valid_data_return_201(self, create_ad_user, auth_ldap_user, authenticate, create_questionnaire):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        response = create_questionnaire(TEST_QUESTIONNAIRE)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0
        assert response.data['name'] == TEST_QUESTIONNAIRE['name']
        assert response.data['description'] == TEST_QUESTIONNAIRE['description']


@pytest.mark.django_db
class TestRetriveQuestionnaire:
    def test_if_user_not_authenticate_returns_401(self, retrieve_questionnaire):
        questionnaire = baker.make(Questionnaire)

        response = retrieve_questionnaire(questionnaire.id)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_authenticated_returns_200(self, create_ad_user, auth_ldap_user, authenticate, retrieve_questionnaire):
        questionnaire = baker.make(Questionnaire)

        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])

        response = retrieve_questionnaire(questionnaire.id)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == questionnaire.id

    def test_if_questionnaire_not_exist_returns_404(self,create_ad_user, auth_ldap_user, authenticate, retrieve_questionnaire):
        questionnaire = baker.make(Questionnaire)

        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])

        response = retrieve_questionnaire(0)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRetriveQuestionnaireList:
    def test_if_user_not_authenticate_returns_401(self, retrieve_questionnaire_list):
        response = retrieve_questionnaire_list()
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_authenticated_returns_200(self, create_ad_user, auth_ldap_user, authenticate, retrieve_questionnaire_list):
        baker.make(Questionnaire, 2)

        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])

        response = retrieve_questionnaire_list()
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
        assert len(response.data["results"]) == 2

    def test_if_questionnaires_not_exist_returns_empty_results(self,create_ad_user, auth_ldap_user, authenticate, retrieve_questionnaire_list):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])

        response = retrieve_questionnaire_list()
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert len(response.data["results"]) == 0


@pytest.mark.django_db
class TestUdpateQuestionnaire:
    def test_if_user_not_authenticate_returns_401(self, update_questionnaire):
        questionnaire = baker.make(Questionnaire)
        response = update_questionnaire(questionnaire.id, TEST_QUESTIONNAIRE)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_authorizated_returns_403(self, create_ad_user, auth_ldap_user, authenticate, update_questionnaire):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])
        
        questionnaire = baker.make(Questionnaire)
        response = update_questionnaire(questionnaire.id, TEST_QUESTIONNAIRE)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_returns_400(self, create_ad_user, auth_ldap_user, authenticate, update_questionnaire):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaire = baker.make(Questionnaire)
        response = update_questionnaire(questionnaire.id, {'name': ''})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_valid_data_returns_200(self, create_ad_user, auth_ldap_user, authenticate, update_questionnaire):
        create_ad_user(TEST_USER)

        auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaire = baker.make(Questionnaire)
        response = update_questionnaire(questionnaire.id, TEST_QUESTIONNAIRE)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
        assert response.data['name'] == TEST_QUESTIONNAIRE['name']
        assert response.data['description'] == TEST_QUESTIONNAIRE['description']

    def test_if_questionnaire_not_exist_returns_404(self, create_ad_user, auth_ldap_user, authenticate, update_questionnaire):
        questionnaire = baker.make(Questionnaire)

        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)

        response = update_questionnaire(0, TEST_QUESTIONNAIRE)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteQuestionnaires:
    def test_if_user_not_authenticate_returns_401(self, delete_questionnaires):
        questionnaires = baker.make(Questionnaire, 2)
        response = delete_questionnaires([questionnaire.id for questionnaire in questionnaires])
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_authorizated_returns_403(self, create_ad_user, auth_ldap_user, authenticate, delete_questionnaires):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])
        
        questionnaires = baker.make(Questionnaire, 2)
        response = delete_questionnaires([questionnaire.id for questionnaire in questionnaires])

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_valid_questionnaires_list_returns_200(self, create_ad_user, auth_ldap_user, authenticate, delete_questionnaires):
        create_ad_user(TEST_USER)

        auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaires = baker.make(Questionnaire, 2)
        response = delete_questionnaires([questionnaire.id for questionnaire in questionnaires])
        
        assert response.status_code == status.HTTP_200_OK
        assert Questionnaire.objects.all().count() == 0

    def test_if_no_valid_questionnaires_list_returns_404(self, create_ad_user, auth_ldap_user, authenticate, delete_questionnaires):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaires = baker.make(Questionnaire, 2)
        response = delete_questionnaires([0, 1])
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
class TestDeactivateQuestionnaires:
    def test_if_user_not_authenticate_returns_401(self, deactivate_questionnaires):
        questionnaires = baker.make(Questionnaire, 2)
        response = deactivate_questionnaires([questionnaire.id for questionnaire in questionnaires])
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_authorizated_returns_403(self, create_ad_user, auth_ldap_user, authenticate, deactivate_questionnaires):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'])
        
        questionnaires = baker.make(Questionnaire, 2)
        response = deactivate_questionnaires([questionnaire.id for questionnaire in questionnaires])

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_valid_questionnaires_list_returns_200(self, create_ad_user, auth_ldap_user, authenticate, deactivate_questionnaires):
        create_ad_user(TEST_USER)

        auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaires = baker.make(Questionnaire, 2)
        response = deactivate_questionnaires([questionnaire.id for questionnaire in questionnaires])
        
        assert response.status_code == status.HTTP_200_OK
        assert Questionnaire.objects.filter(is_active=False).count() == 2

    def test_if_no_valid_questionnaires_list_returns_404(self, create_ad_user, auth_ldap_user, authenticate, deactivate_questionnaires):
        ad_user = create_ad_user(TEST_USER)

        auth_response = auth_ldap_user({
            "username": TEST_USER['username'],
            "password": TEST_USER['password'],
        })

        authenticate(username=TEST_USER['username'], is_staff=True)
        
        questionnaires = baker.make(Questionnaire, 2)
        response = deactivate_questionnaires([0, 1])
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST





