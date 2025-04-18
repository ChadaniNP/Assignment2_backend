# Blog Feature Backend

This repository contains the blog feature implementation for our group project. It includes user authentication, blog post creation, and comprehensive testing.

## Features Implemented

- User Registration
- User Login/Logout with Token Authentication
- Blog Post Creation
- Integration Tests
- Unit Tests

## Getting Started

### 1. Clone and Review the Code

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/ChadaniNP/Assignment2_backend.git

# Switch to the blog feature branch
git checkout 6-as-a-user-i-want-to-create-a-post-so-that-i-can-share-my-blog---backend

# Review the changes in these files:
- blog/models.py - Blog post data model
- blog/views.py - API endpoints
- blog/serializers.py - Data serialization
- blog/urls.py - URL routing
- blog/tests.py - Unit and integration tests
```

### 2. Review the Integration Guide

Check `blog/INTEGRATION_GUIDE.md` for detailed integration steps.

### 3. Set Up Local Development

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test --keepdb
```

### 4. API Endpoints

- POST `/register/` - Register new user
- POST `/login/` - Login and get token
- POST `/create/` - Create blog post (requires authentication)
- POST `/logout/` - Logout (requires authentication)

### 5. Testing the API

```bash
# Example: Register a new user
curl -X POST http://localhost:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","email":"test@example.com"}'

# Example: Login
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'

# Example: Create blog post (replace TOKEN with actual token)
curl -X POST http://localhost:8000/create/ \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Post","content":"This is a test post"}'
```

## Integration Steps

1. Review the code changes
2. Test locally following the steps above
3. Merge the changes into your main branch
4. Update the Vercel deployment

## Database Configuration

This project uses PostgreSQL. Make sure your database settings in `settings.py` match the existing configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neondb',
        # ... other settings
    }
}
```

## Running Tests

```bash
# Run all tests
python manage.py test --keepdb

# Run specific test class
python manage.py test blog.tests.BlogAPIIntegrationTestCase --keepdb

# Run with verbose output
python manage.py test --keepdb -v 2
```

## Deployment

After merging, redeploy to Vercel:

1. Commit and push all changes
2. Go to your Vercel dashboard
3. Trigger a new deployment
4. Verify the endpoints are working

## Need Help?

If you encounter any issues:
1. Check the integration guide
2. Run tests to verify functionality
3. Review the error messages
4. Contact me for clarification

## Contributing

1. Review the code
2. Test locally
3. Provide feedback through GitHub comments
4. Suggest improvements
5. Report any issues
