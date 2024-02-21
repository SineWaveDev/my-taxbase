from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'allow_null': True}, 'is_active': {'allow_null': True}}


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('username', 'mobile', 'password')


