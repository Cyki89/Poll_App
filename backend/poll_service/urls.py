from cgitb import lookup
from django.urls import path
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('voting', views.VotingViewSet, basename="voting")
router.register("questionnaires", views.QuestionnaireViewSet, basename="questionnaires")

questionnaire_router = routers.NestedDefaultRouter(
    router, "questionnaires", lookup="questionnaire"
)
questionnaire_router.register(
    "questions", views.QuestionViewSet, basename="questionnaire-question"
)

question_router = routers.NestedDefaultRouter(
    questionnaire_router, "questions", lookup="question"
)
question_router.register("answers", views.AnswerViewSet, basename="question-answers")

urlpatterns = [
    *router.urls,
    *questionnaire_router.urls,
    *question_router.urls,
]