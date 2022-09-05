from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ADGroupSerializer, ADUserCreateSerializer, ADUserSerializer, ADLoginSerializer
from .models import ADGroup, ADUser


class ADGroupViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = ADGroupSerializer
    queryset = ADGroup.objects.all()


class ADUserViewSet(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ADUser.objects.prefetch_related("groups")

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ADUserCreateSerializer
        return ADUserSerializer


class ADAuthView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ADLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({"user": user}, status.HTTP_200_OK)
