from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, BlogPostSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import BlogPost

class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class BlogPostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data)