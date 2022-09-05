from rest_framework import serializers
from .models import ADGroup, ADUser


class ADGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADGroup
        fields = ["id", "name", "users", "is_active"]


class ADSimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADGroup
        fields = ["id", "name"]


class ADUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ADUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "password",
            "email",
            "is_active",
            "groups",
        ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ADUserSerializer(ADUserCreateSerializer):
    groups = serializers.StringRelatedField(many=True)


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
