from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User, BlogPost

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid username or password')

        # Create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        return {'token': token.key}

class BlogPostSerializer(serializers.ModelSerializer):
    """
    Serializer for BlogPost model. Handles serialization and validation.
    
    The 'fields' attribute lists all model fields that should be exposed via the API.
    The 'read_only_fields' attribute ensures that certain fields (like 'id', 'author', 'created_at')
    are included in API responses but cannot be set or modified by the user. This is important for
    fields that are auto-generated or managed by the system for security and data integrity.
    """
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']
