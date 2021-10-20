from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'token']

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)