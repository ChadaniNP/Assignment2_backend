# views.py - Defines API views for user auth and blog post operations
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import BlogPost
from .serializers import BlogPostSerializer, RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404

class RegisterView(APIView):
    """
    API endpoint for user registration. Accepts username and password, returns auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validate required fields
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check for existing username
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a new user and generate auth token
        user = User.objects.create_user(username=username, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    API endpoint for user login. Returns auth token if credentials are valid.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate auth token for authenticated user
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

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
        # Serialize blog post data
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            # Save blog post with authenticated user as author
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
        # Full update of a blog post
        blog_post = get_object_or_404(BlogPost, pk=pk, author=request.user)
        serializer = BlogPostSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        # Partial update of a blog post
        blog_post = get_object_or_404(BlogPost, pk=pk, author=request.user)
        serializer = BlogPostSerializer(blog_post, data=request.data, partial=True)
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
        # Retrieve blog post to delete
        blog_post = get_object_or_404(BlogPost, pk=pk, author=request.user)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)