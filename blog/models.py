from django.db import models
from django.contrib.auth.models import User
# NOTE: This is a demo change for pull request review purposes.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)