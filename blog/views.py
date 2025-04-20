# views.py - Defines API views for user auth and blog post operations
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import BlogPost
from .serializers import RegisterSerializer, LoginSerializer, BlogPostSerializer
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    """
    API endpoint for user registration. Accepts username and password, returns auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    API endpoint for user login. Returns auth token if credentials are valid.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """
    API endpoint for logging out the authenticated user by deleting their token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete auth token for authenticated user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostCreateView(APIView):
    """
    API endpoint for creating a new blog post. Only authenticated users allowed.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostListView(APIView):
    """
    API endpoint for listing all blog posts of the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve blog posts for authenticated user
        blog_posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)

class BlogPostUpdateView(APIView):
    """
    API endpoint for updating a blog post. Supports full (PUT) and partial (PATCH) updates.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blog_post, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostDeleteView(APIView):
    """
    API endpoint for deleting a blog post by its ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
