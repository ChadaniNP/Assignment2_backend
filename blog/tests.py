from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.authtoken.models import Token

class BlogPostCreateViewTestCase(APITestCase):
    # Test case for creating a new blog post via API
    def setUp(self):
        # Create a test user and authenticate client
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)

    def test_create_blog_post(self):
        # Test creating a new blog post via API
        data = {'title': 'Test Blog Post', 'content': 'This is a test blog post.'}
        response = self.client.post(reverse('blog-post-create'), data, format='json')
        self.assertEqual(response.status_code, 201)  # Expect successful creation
        self.assertEqual(BlogPost.objects.count(), 1)  # One post should exist
        blog_post = BlogPost.objects.get()
        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.author, self.user)

class BlogPostModelTestCase(TestCase):
    # Test case for direct creation of BlogPost model instance
    def setUp(self):
        # Create a test user for model tests
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_create_blog_post(self):
        # Test direct creation of BlogPost model instance
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        self.assertEqual(blog_post.title, 'Test Blog Post')
        self.assertEqual(blog_post.content, 'This is a test blog post.')
        self.assertEqual(blog_post.author, self.user)

class BlogPostSerializerTestCase(TestCase):
    # Test case for serialization of BlogPost instance
    def setUp(self):
        # Create a test user for serializer tests
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_serialize_blog_post(self):
        # Test serialization of BlogPost instance
        blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            content='This is a test blog post.',
            author=self.user
        )
        serializer = BlogPostSerializer(blog_post)
        self.assertEqual(serializer.data['title'], 'Test Blog Post')
        self.assertEqual(serializer.data['content'], 'This is a test blog post.')

class BlogPostUpdateViewTestCase(APITestCase):
    # Test case for updating a blog post via API
    def setUp(self):
        # Create and authenticate user, create initial blog post
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        self.blog_post = BlogPost.objects.create(
            title='Original Title',
            content='Original content.',
            author=self.user
        )

    def test_update_blog_post(self):
        # Test full update (PUT) of a blog post
        url = reverse('blog-post-edit', args=[self.blog_post.id])
        data = {'title': 'Updated Title', 'content': 'Updated content.'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Updated Title')
        self.assertEqual(self.blog_post.content, 'Updated content.')

    def test_update_blog_post_partial(self):
        # Test partial update (PATCH) of a blog post
        url = reverse('blog-post-edit', args=[self.blog_post.id])
        data = {'title': 'Partially Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.blog_post.refresh_from_db()
        self.assertEqual(self.blog_post.title, 'Partially Updated Title')
        self.assertEqual(self.blog_post.content, 'Original content.')

class BlogAPIIntegrationTestCase(APITestCase):
    # Test case for complete blog API integration
    def test_complete_blog_flow(self):
        # 1. Register a new user
        register_data = {
            'username': 'newuser',
            'password': 'newpass123',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('register'), register_data, format='json')
        self.assertEqual(response.status_code, 201)  # User should be created
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
        self.assertIn('token', response.data)  # Token should be present
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

        # 4. Logout and verify token is deleted
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Token.objects.filter(user__username='newuser').exists())

    def test_complete_blog_flow_full(self):
        # 1. Register a new user
        user_data = {'username': 'integrationuser', 'password': 'integrationpass123'}
        response = self.client.post(reverse('register'), user_data, format='json')
        self.assertEqual(response.status_code, 201)

        # 2. Log in and get token
        response = self.client.post(reverse('login'), user_data, format='json')
        self.assertEqual(response.status_code, 200)
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        # 3. Create a blog post
        blog_data = {'title': 'Integration Blog', 'content': 'Integration test content.'}
        response = self.client.post(reverse('blog-post-create'), blog_data, format='json')
        self.assertEqual(response.status_code, 201)
        blog_id = response.data['id']

        # 4. List blog posts (should include the new one)
        response = self.client.get(reverse('blog-post-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(post['id'] == blog_id for post in response.data))

        # 5. Update the blog post
        update_data = {'title': 'Updated Integration Blog', 'content': 'Updated content.'}
        response = self.client.put(reverse('blog-post-edit', args=[blog_id]), update_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Updated Integration Blog')

        # 6. Partial update
        patch_data = {'content': 'Patched content.'}
        response = self.client.patch(reverse('blog-post-edit', args=[blog_id]), patch_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], 'Patched content.')