# serializers.py - Contains serializers for user registration, login, and blog post operations
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User, BlogPost

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user. Handles creation and validation.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a new user with the provided validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login. Validates credentials and returns token.
    """
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
    """
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author']
        read_only_fields = ['id', 'author']