from django.db import transaction
from django.db.models import F
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Questionnaire, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "text", "count"]

    def create(self, validated_data):
        question = Question.objects.get(pk=self.context["question_id"])
        return Answer.objects.create(question=question, **validated_data)


class AnswerUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    count = serializers.IntegerField(read_only=True)
    state = serializers.CharField(write_only=True)


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    votes_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Question
        fields = ["id", "text", "date_added", "answers", 'votes_count']


class QuestionCreateSerializer(serializers.ModelSerializer):
    '''
    {
        "text": "DRF TEXT",
        "answers": [
            {"text" : "text1"},
            {"text" : "text2"},
            {"text" : "text3"}
        ]
    }
    '''
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]
    
    def validate_answers(self, answers):
        if (len(answers)) < 2:
            raise serializers.ValidationError("Each question have to have at leat 2 options")
        return answers

    def create(self, validated_data):
        with transaction.atomic():
            answers = validated_data.pop('answers')
            
            questionnaire = Questionnaire.objects.get(pk=self.context["questionnaire_id"])  
            question = Question.objects.create(questionnaire=questionnaire, **validated_data)
            answer_objs = [Answer(question=question, text=answer['text']) for answer in answers]
            Answer.objects.bulk_create(answer_objs)

        return question


class QuestionUpdateSerializer(serializers.ModelSerializer):
    answers = AnswerUpdateSerializer(many=True)

    def validate_answers(self, answers):
        new_answers = sum(1 for answer in answers if answer['state'] == 'new')
        deleted_answers = sum(1 for answer in answers if answer['state'] == 'deleted')

        if (self.instance.answers_count() + new_answers - deleted_answers) < 2:
            raise serializers.ValidationError("Each question have to have at leat 2 options")
        return answers

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]

    def update(self, instance, validated_data):

        with transaction.atomic():
            instance.text = validated_data.get('text', instance.text)
            instance.save()

            answers = validated_data.get('answers', [])
            for answer in answers:
                state = answer.pop('state')
                if state == 'deleted':
                    Answer.objects.filter(id=answer['id']).delete()
                if state == 'edited':
                    Answer.objects.filter(id=answer['id']).update(text=answer['text'])
                if state == 'new':
                    Answer.objects.create(question=instance, text=answer['text'])

            return instance


class QuestionnaireCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questionnaire
        fields = ["id", "name", "description", "date_added", "is_active"]


class QuestionnaireSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = ["id", "name", "description", "date_added", "is_active", "questions", "users"]


class VotingSerializer(serializers.Serializer):
    """
    {
        "questionnaire_id": 4,
        "user_id" : 6,
        "answers": [
            42,
            43
        ]
    }
    """
    questionnaire_id = serializers.IntegerField(min_value=1)
    answers = serializers.ListField(child=serializers.IntegerField(min_value=1))
    user_id = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        with transaction.atomic():
            questionnaire = get_object_or_404(
                Questionnaire, pk=attrs["questionnaire_id"]
            )

            if questionnaire.is_active == False:
                raise serializers.ValidationError("Voting is not longer active")

            user = get_object_or_404(User, pk=attrs["user_id"])
            if user in questionnaire.users.all():
                raise serializers.ValidationError(
                    "User already check this questionnaire"
                )
            questionnaire.users.add(user)

            answers = attrs["answers"]
            for answer_id in answers:
                answer = get_object_or_404(Answer, pk=answer_id)
                answer.count += 1
                answer.save()

            # Answer.objects.filter(id__in=attrs['answers'])\
            #               .update(count=F('count') + 1)

        return attrs

class QuestionnaireListSerializer(serializers.Serializer):
    questionnaires = serializers.ListField(child=serializers.IntegerField(min_value=1))