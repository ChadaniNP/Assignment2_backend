from django.urls import path
from blog.views import RegisterView, LoginView, LogoutView
from . import views

# NOTE: This is a demo change for pull request review purposes.
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.BlogPostCreateView.as_view(), name='blog-post-create'),
]
