from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.authtoken.models import Token

# NOTE: This is a demo change for pull request review purposes.

class BlogPostCreateViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_blog_post(self):
        data = {'title': 'Test Blog Post', 'content': 'This is a test blog post.'}
        response = self.client.post(reverse('blog-post-create'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.get()
        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.author, self.user)

class BlogPostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_blog_post(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.content, 'This is a test blog post.')
        self.assertEqual(blog_post.author, self.user)

class BlogPostSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_serialize_blog_post(self):
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        serializer = BlogPostSerializer(blog_post)
        self.assertEqual(serializer.data['title'], 'Test Blog Post')
        self.assertEqual(serializer.data['content'], 'This is a test blog post.')

class BlogAPIIntegrationTestCase(APITestCase):
    def test_complete_blog_flow(self):
        # 1. Register a new user
        register_data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('register'), register_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Get the user and verify password is set correctly
        user = User.objects.get(username='newuser')
        self.assertTrue(user.check_password('newpass123'))

        # 2. Login with the new user
        login_data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        if response.status_code != 200:
            print(f"Login failed with response: {response.data}")  # Debug info
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        token = response.data['token']

        # 3. Create a blog post using the token
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        blog_data = {
            'title': 'Integration Test Blog',
            'content': 'This is a blog post created during integration testing.'
        }
        response = self.client.post(reverse('blog-post-create'), blog_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(BlogPost.objects.count(), 1)
        blog_post = BlogPost.objects.get()
        self.assertEqual(blog_post.title, 'Integration Test Blog')
        self.assertEqual(blog_post.author.username, 'newuser')

        # 4. Logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 204)
        # Verify token is deleted
        self.assertFalse(Token.objects.filter(user__username='newuser').exists())