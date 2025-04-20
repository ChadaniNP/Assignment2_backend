from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer, BlogPostSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import BlogPost

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = BlogPostSerializer(data=data)

        if serializer.is_valid():
            post = serializer.save()
            return Response({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'author': post.author.username,
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# List blog posts by the authenticated user
class BlogPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blog_posts = BlogPost.objects.filter(author=request.user)
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlogPostDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response({"detail": "You do not have permission to delete this post."},
                            status=status.HTTP_404_NOT_FOUND)

        blog_post.delete()
        return Response({"detail": "Blog post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
