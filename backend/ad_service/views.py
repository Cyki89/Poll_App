from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ADGroupSerializer, ADUserSerializer, ADLoginSerializer
from .models import ADGroup, ADUser


class ADGroupViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ADGroupSerializer
    queryset = ADGroup.objects.all()


class ADUserViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ADUserSerializer
    queryset = ADUser.objects.prefetch_related("groups")


class ADAuthView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ADLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({"user": user}, status.HTTP_200_OK)
