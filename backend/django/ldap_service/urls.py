from django.urls import path
from .views import LdapTokenObtainPairView, LdapCookieRefreshView, LdapLogoutView

urlpatterns = [
    path("jwt/create/", LdapTokenObtainPairView.as_view()),
    path("jwt/refresh/", LdapCookieRefreshView.as_view()),
    path("logout/", LdapLogoutView.as_view()),
]
