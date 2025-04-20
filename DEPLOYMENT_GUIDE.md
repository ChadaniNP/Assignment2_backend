# Deployment Guide for Blog Feature

Hi teammate! Here's how to review, merge, and deploy the blog feature.

## 1. Review the Code

1. Go to GitHub and review the pull request from the `blog-feature-clean` branch
2. Key files to review:
   - `blog/models.py` - BlogPost model
   - `blog/views.py` - API endpoints
   - `blog/serializers.py` - Data handling
   - `blog/urls.py` - URL routing
   - `blog/tests.py` - Unit and integration tests

## 2. Test Locally

```bash
# Get the latest code
git checkout main
git pull origin main
git checkout blog-feature-clean
git pull origin blog-feature-clean

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Run tests
python manage.py test --keepdb
```

## 3. Merge the Code

1. If all tests pass, merge the pull request on GitHub
2. Delete the `blog-feature-clean` branch after merging

## 4. Deploy to Vercel

1. Go to your Vercel dashboard
2. Select our project
3. Verify these settings:
   - Framework Preset: Django
   - Build Command: `pip install -r requirements.txt`
   - Install Command: None needed
   - Output Directory: Not needed for Django
   - Environment Variables: Make sure database credentials are set

4. Click "Deploy" or wait for auto-deployment

## 5. Verify Deployment

Test these endpoints on the deployed API:

1. Register: POST `/register/`
   ```json
   {
     "username": "testuser",
     "password": "testpass123",
     "email": "test@example.com"
   }
   ```

2. Login: POST `/login/`
   ```json
   {
     "username": "testuser",
     "password": "testpass123"
   }
   ```

3. Create Post: POST `/create/`
   ```json
   {
     "title": "Test Post",
     "content": "This is a test post"
   }
   ```
   Headers: `Authorization: Token <your-token>`

4. Logout: POST `/logout/`
   Headers: `Authorization: Token <your-token>`

## Troubleshooting

If you encounter issues:

1. Database Issues:
   - Check if migrations are applied
   - Verify database credentials in Vercel

2. Authentication Issues:
   - Ensure `REST_FRAMEWORK` settings are correct
   - Check if token authentication is enabled

3. CORS Issues:
   - Verify CORS settings in `settings.py`
   - Check allowed origins

## Need Help?

If you run into any problems:
1. Check the Vercel deployment logs
2. Run tests locally to verify the issue
3. Contact me for assistance

## Rollback Plan

If needed, you can rollback to the previous version:
1. Go to Vercel dashboard
2. Find the last working deployment
3. Click "..." > "Redeploy"
