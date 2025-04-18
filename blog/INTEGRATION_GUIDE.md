# Blog Feature Integration Guide

## Files to Add
1. `blog/models.py` - Contains BlogPost model
2. `blog/views.py` - Contains API views for blog operations
3. `blog/serializers.py` - Contains serializers for blog data
4. `blog/urls.py` - Contains URL routing for blog endpoints
5. `blog/tests.py` - Contains tests for blog functionality

## Integration Steps

1. Add Dependencies
   Add these to your requirements.txt if not already present:
   ```
   django-cors-headers==4.7.0
   djangorestframework==3.16.0
   ```

2. Update INSTALLED_APPS
   Add to your settings.py:
   ```python
   INSTALLED_APPS = [
       ...
       'blog.apps.BlogConfig',
       'rest_framework',
       'rest_framework.authtoken',
       'corsheaders',
   ]
   ```

3. Add URL Configuration
   In your main urls.py, add:
   ```python
   from django.urls import path, include

   urlpatterns = [
       ...
       path('', include('blog.urls')),
   ]
   ```

4. Run Migrations
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## API Endpoints

1. User Registration:
   - URL: `/register/`
   - Method: POST
   - Data: `{"username": "user", "password": "pass", "email": "user@example.com"}`

2. User Login:
   - URL: `/login/`
   - Method: POST
   - Data: `{"username": "user", "password": "pass"}`

3. Create Blog Post:
   - URL: `/create/`
   - Method: POST
   - Headers: `Authorization: Token <your-token>`
   - Data: `{"title": "Post Title", "content": "Post Content"}`

4. Logout:
   - URL: `/logout/`
   - Method: POST
   - Headers: `Authorization: Token <your-token>`

## Testing
Run tests using:
```bash
python manage.py test --keepdb
```

## Database Requirements
- Requires PostgreSQL database
- Uses Django's authentication system
- Creates tables for: User, Token, BlogPost

## Notes
- All blog posts require authentication
- Uses token-based authentication
- CORS is enabled for frontend integration
