from django.db import transaction
from django.contrib.auth.models import User, Group
from django.forms import model_to_dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from djoser.serializers import (
    UserCreateSerializer,
)
from ad_service.models import ADUser
from ad_service.serializers import ADUserSerializer

# TODO Remove if unused and move valide logic to other place
class LdapUserSerializer(UserCreateSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = ["id", "username", "password"]

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = ADUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Ivalid creadentials.")

        return ADUserSerializer(user).data

    def perform_create(self, validated_data):
        with transaction.atomic():
            ad_groups = validated_data.pop("groups")
            password = validated_data.pop("password")

            user = User.objects.create_user(**validated_data)
            user.password = password
            user.save()

            for ad_group in ad_groups:
                group, _ = Group.objects.get_or_create(name=ad_group)
                user.groups.add(group)

        return user



class LdapTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["username"] = user.username
        token["groups"] = (
            None if not (user_groups := user.groups.all()) else 
            [group.name for group in user_groups]
        )

        return token

    def validate(self, attrs):
        ldap_user_serializer = LdapUserSerializer(data=attrs)
        validated_data = ldap_user_serializer.validate(attrs)

        if not (user := User.objects.filter(username=attrs["username"]).first()):
            ldap_user_serializer.perform_create(validated_data)
        else:
            self.update_user_data(validated_data, user)

        return super().validate(attrs)

    def update_user_data(self, ad_props, user):
        ad_password = ad_props.pop("password")
        ad_groups = ad_props.pop("groups")

        self.update_props(user, ad_props, ad_password)
        self.update_groups(user, ad_groups)

    def update_props(self, user, ad_props, ad_password):
        changed = False

        user_props = model_to_dict(user)
        for prop, value in ad_props.items():
            if user_props[prop] != value:
                setattr(user, prop, value)
                changed = True

        if not user.check_password(ad_password):
            user.password = ad_password
            changed = True

        if changed:
            user.save()

    def update_groups(self, user, ad_groups):
        user_groups = [group for group in user.groups.all()]
        for group in user_groups:
            if group.name not in ad_groups:
                user.groups.remove(group)

        user_group_names = [group.name for group in user_groups]
        for ad_group in ad_groups:
            if ad_group not in user_group_names:
                group, _ = Group.objects.get_or_create(name=ad_group)
                user.groups.add(group)
