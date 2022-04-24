from rest_framework import serializers
from .models import ADGroup, ADUser


class ADGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADGroup
        fields = ["id", "name", "users"]


class ADSimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADGroup
        fields = ["id", "name"]


class ADUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = ADUser
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "is_active",
            "groups",
        ]


class ADLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = ADUser
        fields = [
            "username",
            "password",
        ]

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = ADUser.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise serializers.ValidationError("Ivalid creadentials.")

        return ADUserSerializer(user).data
