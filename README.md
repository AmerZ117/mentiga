# 🏢 Mentiga KPI Management System

A comprehensive Django-based Key Performance Indicator (KPI) management system for tracking employee performance, goals, and evaluations.

## 🌟 Features

- **Employee Management**: Complete employee profiles with departments, positions, and reporting structures
- **KPI Tracking**: Set and monitor individual and team KPIs
- **Performance Evaluations**: Conduct regular performance reviews and assessments
- **Goal Management**: Set, track, and manage employee goals
- **Training Management**: Track employee training and development
- **Reporting**: Generate comprehensive reports and analytics
- **Modern UI**: Beautiful, responsive interface built with Bootstrap

## 🚀 Quick Deploy to Railway

### Option 1: Automated Deployment (Recommended)

1. **Run the quick deploy script**:
   ```bash
   python quick_deploy.py
   ```

2. **Follow the interactive prompts** to:
   - Create a GitHub repository
   - Set up Git and push your code
   - Install Railway CLI
   - Deploy to Railway automatically

### Option 2: Manual Deployment

1. **Install prerequisites**:
   - [Node.js](https://nodejs.org/) (for Railway CLI)
   - [Git](https://git-scm.com/download/win) (optional, for version control)

2. **Create GitHub repository**:
   - Go to https://github.com/new
   - Name it `mentiga-kpi-system`
   - Make it public

3. **Deploy to Railway**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Initialize and deploy
   railway init
   railway up
   ```

4. **Configure environment variables** in Railway dashboard:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=your-app-name.railway.app
   ```

5. **Run database setup**:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   python manage.py createsuperuser
   ```

## 📁 Project Structure

```
mentiga/
├── config/                 # Django project settings
│   ├── settings.py        # Production-ready settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI application
├── KPI/                   # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── forms.py          # Form definitions
│   ├── admin.py          # Admin interface
│   ├── urls.py           # App URL patterns
│   └── templates/        # HTML templates
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment configuration
├── runtime.txt           # Python version
├── .gitignore           # Git ignore rules
├── deploy.py            # General deployment helper
├── railway_deploy.py    # Railway-specific deployment helper
├── quick_deploy.py      # Automated deployment script
└── README.md            # This file
```

## 🛠️ Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd mentiga
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Main app: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## 📊 Database Models

### Employee
- Personal information (name, email, phone)
- Employment details (position, department, hire date)
- Reporting structure (manager)
- Status tracking (active, inactive, terminated)

### Department
- Department name and description
- Employee relationships

### KPI
- Performance indicators linked to employees
- Target values and actual achievements
- Evaluation periods

### Evaluation
- Performance reviews
- Rating systems
- Comments and feedback

### Goal
- Employee goals and objectives
- Progress tracking
- Due dates and completion status

### Training
- Training programs and courses
- Employee participation tracking
- Completion certificates

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, professional Bootstrap-based design
- **Interactive Elements**: Search, filter, and sort functionality
- **Data Visualization**: Charts and graphs for performance metrics
- **User-Friendly**: Intuitive navigation and clear information hierarchy

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set these in your hosting platform:

```env
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://username:password@host:port/database
```

### Customization

- **Company Branding**: Update colors and logos in templates
- **KPI Categories**: Modify KPI types and evaluation criteria
- **User Roles**: Add custom user roles and permissions
- **Reporting**: Customize report templates and metrics

## 🚀 Deployment Options

### Railway (Recommended)
- Free tier available
- Easy deployment
- Automatic HTTPS
- PostgreSQL database included

### Render
- Free tier available
- Good for Django apps
- Automatic deployments

### Heroku
- Well-established platform
- Good documentation
- Easy scaling

### DigitalOcean App Platform
- Starting at $5/month
- Excellent performance
- Professional grade

## 📚 Documentation

- [Railway Deployment Guide](RAILWAY_DEPLOYMENT.md) - Detailed Railway deployment instructions
- [General Deployment Guide](DEPLOYMENT_GUIDE.md) - Other hosting options
- [Django Documentation](https://docs.djangoproject.com/) - Django framework docs

## 🛠️ Development Tools

### Helper Scripts

- `deploy.py` - General deployment tasks
- `railway_deploy.py` - Railway-specific deployment
- `quick_deploy.py` - Automated full deployment process

### Management Commands

- `python manage.py populate_sample_data` - Add sample data for testing
- `python manage.py collectstatic` - Collect static files for production
- `python manage.py migrate` - Apply database migrations

## 🔒 Security Features

- **Environment Variables**: Sensitive data stored securely
- **CSRF Protection**: Built-in Django security
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **HTTPS**: Automatic SSL certificates on Railway

## 📈 Performance Optimization

- **Static File Compression**: WhiteNoise middleware
- **Database Optimization**: Efficient queries and indexing
- **Caching**: Ready for Redis/memcached integration
- **CDN Ready**: Static files optimized for CDN delivery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter issues:

1. Check the deployment guides
2. Review Django documentation
3. Check application logs
4. Verify environment variables
5. Ensure all dependencies are installed

## 🎉 Success Stories

This KPI system is designed to help organizations:
- ✅ Track employee performance effectively
- ✅ Set and achieve organizational goals
- ✅ Improve team productivity
- ✅ Make data-driven decisions
- ✅ Streamline performance reviews

---

**Ready to deploy?** Run `python quick_deploy.py` to get started with Railway deployment!