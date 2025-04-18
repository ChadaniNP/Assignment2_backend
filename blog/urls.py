from django.urls import path
from blog.views import RegisterView, LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', views.BlogPostCreateView.as_view(), name='blog-post-create'),
]
