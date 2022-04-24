from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from poll_service.permissions import IsAdminOrReadOnly
from .serializers import (
    QuestionnaireListSerializer,
    QuestionnaireSerializer,
    QuestionnaireCreateSerializer,
    QuestionSerializer,
    QuestionCreateSerializer,
    QuestionUpdateSerializer,
    AnswerSerializer,
    VotingSerializer,
)
from .models import Questionnaire, Question, Answer


class QuestionnaireViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'date_added', 'questions_count', 'answers_count']
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuestionnaireCreateSerializer
        return QuestionnaireSerializer

    def get_queryset(self):
        if self.request.method == "POST":
            return Questionnaire.objects.all()
        return (
            Questionnaire.objects
                .prefetch_related("questions__answers", "users")
                .annotate(answers_count=Count('users'))
                .annotate(questions_count=Count('question'))
        )
    
    @action(detail=False, methods=['POST'])
    def delete(self, request):
        serializer = QuestionnaireListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        questionnaires = serializer.data['questionnaires']
        Questionnaire.objects.filter(pk__in=questionnaires).delete()

        return Response(
            {"msg": "Successfully Deleted"}, 
            status.HTTP_200_OK
        )

    @action(detail=False, methods=['POST'])
    def activate(self, request):
        serializer = QuestionnaireListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        questionnaires = serializer.data['questionnaires']
        Questionnaire.objects.filter(pk__in=questionnaires).update(is_active=True)

        return Response(
            {"msg": "Successfully Updated"}, 
            status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['POST'])
    def deactivate(self, request):
        serializer = QuestionnaireListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        questionnaires = serializer.data['questionnaires']
        Questionnaire.objects.filter(pk__in=questionnaires).update(is_active=False)

        return Response(
            {"msg": "Successfully Updated"}, 
            status.HTTP_200_OK
        )


class VotingViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['name', 'date_added']
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return VotingSerializer
        return QuestionnaireSerializer
    
    def get_queryset(self):
        if self.request.method == "POST":
            return Questionnaire.objects.all()
        return (
            Questionnaire.objects
                         .filter(is_active=True)
                         .exclude(users=self.request.user)
                         .prefetch_related("questions__answers", "users")
        )

    def create(self, request, *args, **kwargs):
        serializer = VotingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
       
        return Response(
            status=status.HTTP_204_NO_CONTENT,
            headers=headers
        )
        

class MultiCreateObjectViewSetMixin:
    """
    [
        { "text": "Text For Question 1" },
        { "text": "Text For Question 2" },
        { "text": "Text For Question 3" }
    ]
    [
        { "text": "Answer 1 For Question 1 Questionnary 1" },
        { "text": "Answer 2 For Question 1 Questionnary 1" },
        { "text": "Answer 3 For Question 1 Questionnary 1" }
    ]
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, many=isinstance(request.data, list)
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class QuestionViewSet(MultiCreateObjectViewSetMixin, ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return QuestionCreateSerializer
        if self.request.method == "PATCH":
            return QuestionUpdateSerializer
        return QuestionSerializer

    def get_serializer_context(self):
        return {"questionnaire_id": self.kwargs["questionnaire_pk"]}

    def get_queryset(self):
        return (
            Question.objects
            .filter(questionnaire_id=self.kwargs["questionnaire_pk"])
            .prefetch_related('answers')
        )


class AnswerViewSet(MultiCreateObjectViewSetMixin, ModelViewSet):
    serializer_class = AnswerSerializer

    def get_serializer_context(self):
        return {"question_id": self.kwargs["question_pk"]}

    def get_queryset(self):
        return Answer.objects.filter(question_id=self.kwargs["question_pk"])
