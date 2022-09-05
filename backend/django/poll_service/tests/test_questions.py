from rest_framework import status
from model_bakery import baker
import pytest

from poll_service.models import Question, Questionnaire


TEST_QUESTIONNAIRE = {
    "name": "test_name",
}

TEST_QUESTION =  {
    "text": "DRF text",
    "answers": [
        {"text" : "text1"},
        {"text" : "text2"},
        {"text" : "text3"}
    ]
}

TEST_UPDATE_QUESTION =  {
    "text": "updated"
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
def auth_user(create_ad_user, auth_ldap_user, authenticate):
    def do_auth_user(user, is_staff=False):
        create_ad_user(user)

        auth_ldap_user({
            "username": user['username'],
            "password": user['password'],
        })

        authenticate(username=user['username'], is_staff=is_staff)
    return do_auth_user


@pytest.fixture
def create_questionnaire(api_client):
    def do_create_questionnaire(questionnaire):
        return api_client.post('/poll/questionnaires/', questionnaire)
    return do_create_questionnaire


@pytest.fixture
def create_questions(api_client):
    def do_create_questions(id, question):
        return api_client.post(f"/poll/questionnaires/{id}/questions/", question)
    return do_create_questions


@pytest.fixture
def retrieve_question(api_client):
    def do_retrieve_question(questionnaire_id, question_id):
        return api_client.get(f"/poll/questionnaires/{questionnaire_id}/questions/{question_id}/")
    return do_retrieve_question


@pytest.fixture
def update_question(api_client):
    def do_update_question(questionnaire_id, question_id, data):
        return api_client.patch(f"/poll/questionnaires/{questionnaire_id}/questions/{question_id}/", data)
    return do_update_question


@pytest.mark.django_db
class TestCreateQuestions:
    def test_if_user_not_authenticate_returns_401(self, create_questions):
        questionnaire = baker.make(Questionnaire)
        response = create_questions(questionnaire.id, TEST_QUESTION)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_not_authorizated_returns_403(self, auth_user ,create_questions):
        auth_user(TEST_USER) 

        questionnaire = baker.make(Questionnaire)
        response = create_questions(questionnaire.id, TEST_QUESTION)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_invalid_data_return_400(self, auth_user, create_questions):
        auth_user(TEST_USER, is_staff=True)

        questionnaire = baker.make(Questionnaire)
        response = create_questions(questionnaire.id, TEST_QUESTION)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    # def test_if_valid_data_return_200(self, auth_user, create_questions):
    #     auth_user(TEST_USER, is_staff=True)

    #     questionnaire = baker.make(Questionnaire)
    #     response = create_questions(questionnaire.id, TEST_QUESTION)
    #     print(response.data)
     
    #     assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestRetriveQuestion:
    def test_if_user_not_authenticate_returns_401(self, retrieve_question):
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = retrieve_question(questionnaire.id, question.id)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_authenticated_returns_200(self, auth_user, retrieve_question):
        auth_user(TEST_USER)
        
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = retrieve_question(questionnaire.id, question.id)
        
        assert response.status_code == status.HTTP_200_OK
 
    def test_if_questionnaire_or_question_not_exist_returns_404(self, auth_user, retrieve_question):
        auth_user(TEST_USER)
        
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = retrieve_question(0, question)  
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = retrieve_question(questionnaire.id, 0)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUpdateQuestion:
    def test_if_user_not_authenticate_returns_401(self, update_question):
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = update_question(questionnaire.id, question.id, {})
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_unauthorizated_returns_403(self, auth_user, update_question):
        auth_user(TEST_USER)
        
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = update_question(questionnaire.id, question.id, TEST_UPDATE_QUESTION)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_authorizated_returns_200(self, auth_user, update_question):
        auth_user(TEST_USER, is_staff=True)
        
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = update_question(questionnaire.id, question.id, TEST_UPDATE_QUESTION)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['text'] == TEST_UPDATE_QUESTION['text']

    def test_if_invalid_data_returns_400(self, auth_user, update_question):
        auth_user(TEST_USER, is_staff=True)
        
        questionnaire = baker.make(Questionnaire)
        question = baker.make(Question, questionnaire_id=questionnaire.id)

        response = update_question(questionnaire.id, question.id, {"text": ""})
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
