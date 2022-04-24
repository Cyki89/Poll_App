from django.urls import path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register("groups", views.ADGroupViewSet)
router.register("users", views.ADUserViewSet)

urlpatterns = [*router.urls, path("auth", views.ADAuthView.as_view(), name="auth")]
