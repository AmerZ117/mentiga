# 🚂 Railway Deployment Guide for Django KPI

This guide will walk you through deploying your Django KPI management system to Railway step by step.

## 📋 Prerequisites

Before starting, make sure you have:
- [ ] A GitHub account
- [ ] Node.js installed (for Railway CLI)
- [ ] Your Django project ready

## 🚀 Step-by-Step Deployment

### Step 1: Install Railway CLI

1. **Install Node.js** (if not already installed):
   - Go to https://nodejs.org/
   - Download and install the LTS version

2. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

3. **Login to Railway**:
   ```bash
   railway login
   ```

### Step 2: Prepare Your Code

Your project is already configured with:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Python version
- ✅ Updated `settings.py` - Production-ready configuration
- ✅ `.gitignore` - Excludes sensitive files

### Step 3: Create GitHub Repository

1. **Go to GitHub.com** and create a new repository
2. **Name it** something like `mentiga-kpi-system`
3. **Make it public** (Railway works better with public repos)
4. **Don't initialize** with README (we'll push existing code)

### Step 4: Push Code to GitHub

If you have Git installed:
```bash
git init
git add .
git commit -m "Initial commit - Django KPI system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

If you don't have Git installed:
1. **Download GitHub Desktop** from https://desktop.github.com/
2. **Clone your repository** to your local machine
3. **Copy all your project files** to the repository folder
4. **Commit and push** using GitHub Desktop

### Step 5: Deploy to Railway

#### Option A: Using Railway Dashboard (Recommended for beginners)

1. **Go to Railway.app** and sign up/login
2. **Click "New Project"**
3. **Select "Deploy from GitHub repo"**
4. **Connect your GitHub account** if not already connected
5. **Select your repository** (mentiga-kpi-system)
6. **Railway will automatically detect** it's a Python app

#### Option B: Using Railway CLI

1. **Navigate to your project directory**:
   ```bash
   cd mentiga
   ```

2. **Initialize Railway project**:
   ```bash
   railway init
   ```

3. **Deploy your app**:
   ```bash
   railway up
   ```

### Step 6: Configure Environment Variables

In Railway dashboard:

1. **Go to your project**
2. **Click on "Variables" tab**
3. **Add these environment variables**:

```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,your-custom-domain.com
```

**To generate a secret key**, run:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 7: Add Database (Optional but Recommended)

1. **In Railway dashboard**, click "New"
2. **Select "Database"** → "PostgreSQL"
3. **Railway will automatically** provide the `DATABASE_URL` environment variable

### Step 8: Run Database Migrations

1. **Go to your deployment** in Railway dashboard
2. **Click on "Deployments" tab**
3. **Click on the latest deployment**
4. **Go to "Logs" tab**
5. **Run these commands**:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 9: Access Your Application

1. **Railway will provide** a URL like: `https://your-app-name.railway.app`
2. **Your KPI system** will be accessible at this URL
3. **Admin panel** will be at: `https://your-app-name.railway.app/admin/`

## 🔧 Custom Domain (Optional)

To use your own domain:

1. **In Railway dashboard**, go to "Settings"
2. **Click "Custom Domains"**
3. **Add your domain** (e.g., `kpi.yourcompany.com`)
4. **Update your DNS settings** as instructed by Railway
5. **Update `ALLOWED_HOSTS`** to include your custom domain

## 🛠️ Using the Deployment Helper Script

I've created a helper script for you:

```bash
python railway_deploy.py
```

This script will:
- ✅ Check if Railway CLI is installed
- ✅ Generate secret keys
- ✅ Set environment variables
- ✅ Deploy your application
- ✅ Show deployment status

## 📊 Monitoring Your Deployment

### View Logs
- Go to Railway dashboard
- Click on your project
- Go to "Deployments" tab
- Click on any deployment to view logs

### Health Check
Add this to your `config/urls.py`:
```python
from django.http import HttpResponse

def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    # ... your other URLs
    path('health/', health_check, name='health_check'),
]
```

Then check: `https://your-app-name.railway.app/health/`

## 🔒 Security Best Practices

1. **Never commit sensitive data** to Git
2. **Use environment variables** for all secrets
3. **Keep your dependencies updated**
4. **Regularly backup your database**
5. **Monitor your application logs**

## 🆘 Troubleshooting

### Common Issues:

1. **Build fails**
   - Check `requirements.txt` for correct dependencies
   - Ensure `Procfile` is in the root directory
   - Check Railway logs for specific errors

2. **Database connection errors**
   - Verify `DATABASE_URL` is set correctly
   - Run migrations: `python manage.py migrate`

3. **Static files not loading**
   - Run: `python manage.py collectstatic --noinput`
   - Check `STATIC_ROOT` and `STATIC_URL` settings

4. **500 Internal Server Error**
   - Check Railway logs
   - Verify `DEBUG = False` in production
   - Check `ALLOWED_HOSTS` includes your domain

5. **App not starting**
   - Check `Procfile` syntax
   - Verify `runtime.txt` has correct Python version
   - Check Railway logs for startup errors

### Getting Help

1. **Check Railway documentation**: https://docs.railway.app/
2. **View your application logs** in Railway dashboard
3. **Check Django deployment documentation**
4. **Verify all environment variables** are set correctly

## 🎉 Success!

Once deployed, your KPI management system will be:
- ✅ Accessible from anywhere with an internet connection
- ✅ Automatically updated when you push to GitHub
- ✅ Running on a production-ready server
- ✅ Protected with HTTPS
- ✅ Scalable as your needs grow

## 📈 Next Steps

After successful deployment:

1. **Test all functionality** on the live site
2. **Set up monitoring** and alerts
3. **Configure backups** for your database
4. **Set up CI/CD** for automatic deployments
5. **Add custom domain** if needed
6. **Set up SSL certificates** (automatic with Railway)

## 💰 Railway Pricing

- **Free tier**: $5 credit monthly (usually enough for small projects)
- **Pro plan**: $20/month for more resources
- **Enterprise**: Custom pricing for large organizations

Your KPI system should run comfortably on the free tier!

---

**Need help?** Check the Railway documentation or your deployment logs for specific error messages.
