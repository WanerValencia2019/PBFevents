from random import random
from uuid import uuid4
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

# custom validators
from .validators import secure_password

User = get_user_model()


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions"]


class RegisterSerializer(serializers.Serializer):
    identification = serializers.CharField(max_length=12, required=False)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, validators=[secure_password])

    def create(self, validated_data):
        username = validated_data.get('username', None)
        first_name = validated_data.get('first_name', None)
        last_name = validated_data.get('last_name', None)
        email = validated_data.get('email', None)
        password = validated_data.get('password', None)
        identification = validated_data.get('identification', uuid4().hex[0:12])
        user = User(username=username, first_name=first_name, last_name=last_name, email=email, identification=identification)
        user.set_password(password)
        user.save()
        return user

    def validate(self, data):
        print(data)
        #username = data.get('username', None)
        email = data.get('email', None)
        #if User.objects.filter(username=username).first():
        #    raise ValidationError({'message': 'Este usuario no está disponible'})
        if User.objects.filter(email=email).first():
            raise ValidationError({'message': 'Este correo electrónico no está disponible'})
        return data
