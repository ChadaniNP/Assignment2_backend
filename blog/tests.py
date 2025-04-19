from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import BlogPost
from .serializers import BlogPostSerializer
from rest_framework.authtoken.models import Token

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

class BlogPostDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='deleteuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.blog_post = BlogPost.objects.create(
            title='Delete Me',
            content='Please delete this post',
            author=self.user
        )

    def test_user_can_delete_own_blog_post(self):
        response = self.client.delete(
            reverse('blog-post-delete', kwargs={'pk': self.blog_post.id})
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BlogPost.objects.filter(id=self.blog_post.id).exists())

    def test_user_cannot_delete_others_blog_post(self):
        other_user = User.objects.create_user(username='otheruser', password='pass1234')
        other_post = BlogPost.objects.create(
            title='Not yours!',
            content='Cannot delete this!',
            author=other_user
        )
        response = self.client.delete(
            reverse('blog-post-delete', kwargs={'pk': other_post.id})
        )
        self.assertEqual(response.status_code, 404)  # Because filtered queryset hides it

    def test_complete_blog_flow(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_login(user)

        blog_data = {
            'title': 'Integration Test Blog',
            'content': 'Some test content',
            'author': user.id  # or whatever your view expects
        }

        response = self.client.post(reverse('blog-post-create'), blog_data, format='json')
        self.assertEqual(response.status_code, 201)

        blog_post_id = BlogPost.objects.get(title='Integration Test Blog').id

        # Now test deleting it
        delete_response = self.client.delete(reverse('blog-post-delete', args=[blog_post_id]))
        self.assertEqual(delete_response.status_code, 204)

# for unit tests of like post
class LikePostTests(APITestCase):
    from rest_framework.authtoken.models import Token

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.post = BlogPost.objects.create(title='Test Post', content='Sample content', author=self.user)
        self.like_url = reverse('blog-post-like', kwargs={'post_id': self.post.id})

    def test_like_post(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'post liked')

    def test_unlike_post(self):
        self.post.likes.add(self.user)  # Pre-like the post
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'post unliked')

    def test_like_nonexistent_post(self):
        wrong_url = reverse('blog-post-like', kwargs={'post_id': 999})
        response = self.client.post(wrong_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_like_post_unauthenticated(self):
        self.client.logout()
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# for integration testing
class LikePostFlowTest(APITestCase):

    def test_complete_like_flow(self):
        # Register
        self.client.post('/api/register/', {
            'username': 'newuser',
            'email': 'user@example.com',
            'password': 'strongpassword'
        })

        # Login
        response = self.client.post('/api/login/', {
            'username': 'newuser',
            'password': 'strongpassword'
        })
        token = response.data.get('token')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # Create Post
        response = self.client.post('/api/create/', {
            'title': 'Integration Test Post',
            'content': 'This is an integration test post'
        })
        post_id = response.data['id']

        # Like Post
        response = self.client.post(f'/api/blogs/{post_id}/like/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'post liked')

        # Unlike Post
        response = self.client.post(f'/api/blogs/{post_id}/like/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'post unliked')
