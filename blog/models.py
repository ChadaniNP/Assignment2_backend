# models.py - Defines the database models for the blog app
from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    # Represents a blog post created by a user
    title = models.CharField(max_length=200)  # Title of the blog post
    content = models.TextField()              # Content/body of the blog post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the post's author
    created_at = models.DateTimeField(auto_now_add=True)        # Timestamp of creation
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
