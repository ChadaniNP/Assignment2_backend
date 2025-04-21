from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer, BlogPostSerializer
from .models import BlogPost
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action

# Register a new user
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User login view
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User logout view
class LogoutView(APIView):
    """
    API endpoint for logging out the authenticated user by deleting their token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete auth token for authenticated user
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create a new blog post
class BlogPostCreateView(APIView):
    """
    API endpoint for creating a new blog post. Only authenticated users allowed.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data, context={'request': request})
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = BlogPostSerializer(data=data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            post = serializer.save()
            return Response({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
            }, status=status.HTTP_201_CREATED)

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

# List blog posts by the authenticated user
class BlogPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blog_posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlogPostDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_404_NOT_FOUND)

        blog_post.delete()
        return Response({"detail": "Blog post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class LikePostView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can like the post

    def post(self, request, post_id):
        try:
            post = BlogPost.objects.get(id=post_id)
        except BlogPost.DoesNotExist:
            return Response({'detail': 'Post not found.'}, status=404)

        # Check if the user has already liked the post
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            return Response({'status': 'post unliked'})
        else:
            post.likes.add(request.user)
            return Response({'status': 'post liked'})
        print("Looking for post ID:", post_id)
        print("Available posts:", BlogPost.objects.all())
