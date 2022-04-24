from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LdapTokenObtainPairSerializer


class LdapTokenObtainPairView(TokenObtainPairView):
    serializer_class = LdapTokenObtainPairSerializer
