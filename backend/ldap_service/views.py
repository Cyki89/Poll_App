from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.conf import settings
from .serializers import LdapTokenObtainPairSerializer, LdapCookieRefreshSerializer


class LdapTokenObtainPairView(TokenObtainPairView):
    serializer_class = LdapTokenObtainPairSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            response.set_cookie(
                'refresh_token', 
                response.data['refresh'], 
                max_age = settings.SIMPLE_JWT['AUTH_COOKIE_LIFETIME'], 
                httponly=True 
            )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class LdapCookieRefreshView(TokenRefreshView):
    serializer_class = LdapCookieRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = settings.SIMPLE_JWT['AUTH_COOKIE_LIFETIME']
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']

        return super().finalize_response(request, response, *args, **kwargs)


class LdapLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({}, status.HTTP_204_NO_CONTENT)
        response.delete_cookie('refresh_token')
        return response
