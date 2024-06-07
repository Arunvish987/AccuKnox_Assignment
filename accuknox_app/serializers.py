from rest_framework import serializers
from .models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        return value.lower()

    # def create(self, validated_data):
    #     return UserModel.objects.create_user(**validated_data)
