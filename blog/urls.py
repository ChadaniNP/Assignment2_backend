from django.urls import path
from blog.views import RegisterView, LoginView, LogoutView, BlogPostCreateView, BlogPostListView, BlogPostDeleteView, \
    LikePostView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', BlogPostCreateView.as_view(), name='blog-post-create'),
    path('blogs/', BlogPostListView.as_view(), name='blog-post-list'),
    path('blogs/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog-post-delete'),
    path('blogs/<int:post_id>/like/', LikePostView.as_view(), name='blog-post-like'),

]