# Django KPI Website Deployment Guide

This guide will help you deploy your Django KPI management system to various hosting platforms.

## 🚀 Quick Start - Railway (Recommended for Beginners)

### Step 1: Prepare Your Code
Your project is already configured for deployment with the necessary files:
- `requirements.txt` - Python dependencies
- `Procfile` - Tells the server how to run your app
- `runtime.txt` - Python version
- Updated `settings.py` - Production-ready configuration

### Step 2: Deploy to Railway

1. **Create a Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Connect Your Repository**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your repository

3. **Configure Environment Variables**
   In Railway dashboard, add these environment variables:
   ```
   SECRET_KEY=your-super-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app,your-custom-domain.com
   DATABASE_URL=postgresql://... (Railway will provide this)
   ```

4. **Deploy**
   - Railway will automatically detect it's a Python app
   - It will install dependencies from `requirements.txt`
   - Your app will be deployed!

5. **Run Migrations**
   - In Railway dashboard, go to your app
   - Click on "Deployments" tab
   - Click on the latest deployment
   - Go to "Logs" and run:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

### Step 3: Custom Domain (Optional)
1. In Railway dashboard, go to "Settings"
2. Click "Custom Domains"
3. Add your domain (e.g., `kpi.yourcompany.com`)
4. Update your DNS settings as instructed

## 🌐 Alternative Hosting Options

### Option 1: Render (Free Tier Available)

1. **Sign up at [render.com](https://render.com)**
2. **Create a new Web Service**
3. **Connect your GitHub repository**
4. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`
   - Environment Variables: Same as Railway

### Option 2: Heroku (Paid)

1. **Install Heroku CLI**
2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-kpi-app
   ```
3. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```
4. **Run migrations:**
   ```bash
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```

### Option 3: DigitalOcean App Platform ($5/month)

1. **Create account at [digitalocean.com](https://digitalocean.com)**
2. **Create new App**
3. **Connect GitHub repository**
4. **Configure environment variables**
5. **Deploy**

## 🔧 Production Checklist

Before deploying, ensure:

- [ ] `DEBUG = False` in production
- [ ] Strong `SECRET_KEY` is set
- [ ] `ALLOWED_HOSTS` includes your domain
- [ ] Database is configured (PostgreSQL recommended)
- [ ] Static files are collected
- [ ] Environment variables are set
- [ ] HTTPS is enabled (automatic on most platforms)

## 🛠️ Local Testing Before Deployment

Test your production settings locally:

```bash
# Set environment variables
export SECRET_KEY="your-secret-key"
export DEBUG="False"
export ALLOWED_HOSTS="localhost,127.0.0.1"

# Run with production settings
python manage.py collectstatic --noinput
python manage.py runserver
```

## 📊 Monitoring and Maintenance

### Health Checks
Add this to your `urls.py`:
```python
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    # ... your other URLs
    path('health/', health_check, name='health_check'),
]
```

### Logging
Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## 🔒 Security Best Practices

1. **Never commit sensitive data** (SECRET_KEY, database passwords)
2. **Use environment variables** for all sensitive settings
3. **Enable HTTPS** (automatic on most platforms)
4. **Regular security updates** for dependencies
5. **Backup your database** regularly

## 🆘 Troubleshooting

### Common Issues:

1. **Static files not loading**
   - Run `python manage.py collectstatic --noinput`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

2. **Database connection errors**
   - Verify `DATABASE_URL` environment variable
   - Check database credentials

3. **500 Internal Server Error**
   - Check logs in your hosting platform
   - Verify `DEBUG = False` in production
   - Check `ALLOWED_HOSTS` includes your domain

4. **Migration errors**
   - Run `python manage.py migrate` on the server
   - Check for conflicting migrations

## 📞 Support

If you encounter issues:
1. Check the hosting platform's documentation
2. Review Django deployment documentation
3. Check the logs in your hosting platform's dashboard
4. Ensure all environment variables are set correctly

## 🎉 Success!

Once deployed, your KPI management system will be accessible at your custom URL, and you can:
- Manage employees and their performance
- Track KPIs and evaluations
- Generate reports
- Access the system from anywhere with an internet connection

Remember to regularly backup your data and keep your dependencies updated!
