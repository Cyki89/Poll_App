from django.urls import path
from .views import LdapTokenObtainPairView

urlpatterns = [
    path("jwt/create/", LdapTokenObtainPairView.as_view()),
]
