from django.contrib.auth.hashers import make_password
from .models import User

from rest_framework.serializers import (
    ModelSerializer,
    DateField,
    DateTimeField,
)
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(ModelSerializer):
    created_at = DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)
    updated_at = DateTimeField(format='%d-%m-%Y %H:%M:%S', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'is_staff',
            'is_superuser',
            'is_customer',
            'password',
            'created_at',
            'updated_at',
            'first_name', 
            'last_name'
        ]
        read_only_fields = ('is_active', 'created_at', 'updated_at', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        validated_data['username'] = validated_data['email']
        validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
    def to_representation(self, instance: User):
        serialized_self = dict(super().to_representation(instance))
        if instance.is_superuser:
            serialized_self['user_type'] = "super admin"
        elif instance.is_staff:
            serialized_self['user_type'] = 'staff'
        else:
            serialized_self['user_type'] = 'customer'
        
        return serialized_self


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get('password')
        }
        user_obj = User.objects.filter(email=attrs.get('username')).first() or User.objects.filter(username=attrs.get('username')).first()
        if user_obj:
            credentials['username'] = user_obj.username
            data = super().validate(credentials)
            user_serializer = UserSerializer(user_obj)
            user_data = user_serializer.data
            user_data['token'] = data
        else:
            raise exceptions.NotFound(
                "User not found"
            )
        
        return user_data