from django.contrib.auth.models import User
from rest_framework import serializers

from electronics.models import Electronica


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'phone', 'last_name', 'first_name', 'money']


class ElectronicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Electronica
        fields = ['id', 'name', 'brand', 'image', 'price', 'description', 'created_at', 'count']
