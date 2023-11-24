from rest_framework import serializers
from .models import *


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank_Info
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=500)
    class Meta:
        model = User
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['password'] = make_password(validated_data.get('password'))
    #     return super(UserSerializer, self).create(validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'email')



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=500)