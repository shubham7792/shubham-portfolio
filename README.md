# 🚀 Developer Portfolio — Django Full Stack

A modern, professional developer portfolio built with Django, featuring OAuth, JWT authentication, project showcase, and a stunning dark theme UI.

## ✨ Features

- **Authentication**: Django auth + OAuth (Google/GitHub) + JWT API tokens
- **Public Home**: Hero section with profile, social links, CV download
- **About** (auth required): Skills with animated bars, timeline experience/education
- **Projects** (auth required): Filterable project grid with tech tags
- **Contact** (auth required): Contact form saved to database
- **Admin Panel**: Manage everything via `/admin/`
- **REST API**: JWT-protected endpoints at `/api/`
- **Responsive**: Mobile-first design

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2+ |
| Database | PostgreSQL |
| Auth | Django + AllAuth (OAuth) + SimpleJWT |
| API | Django REST Framework |
| Frontend | HTML5, CSS3 (custom), JavaScript (vanilla) |
| Fonts | Syne + DM Sans (Google Fonts) |
| Icons | FontAwesome 6 |
| Storage | WhiteNoise (static) |

## 📁 Project Structure

```
portfolio_project/
├── portfolio_project/     # Core settings, urls, wsgi
├── portfolio/             # Home, About, Profile models
├── projects/              # Projects CRUD
├── contact/               # Contact form & messages
├── accounts/              # Auth views, JWT
├── templates/             # Base template + auth templates
├── static/
│   ├── css/main.css       # Complete design system
│   └── js/main.js         # Interactions & animations
├── media/                 # Uploaded files (cv, images)
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone <your-repo>
cd portfolio_project
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file (or set env vars):

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=portfolio_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

# OAuth (optional - get from Google/GitHub developer consoles)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

CONTACT_EMAIL=your@email.com
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb portfolio_db

# Run migrations
python manage.py migrate

# Seed demo data
python manage.py seed_data

# Create admin superuser
python manage.py createsuperuser
```

### 4. Collect Static & Run

```bash
python manage.py collectstatic --no-input
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## 🔑 Authentication

### Session Auth (Web)
- Register: `/accounts/register/`
- Login: `/accounts/login/`
- OAuth: `/accounts/google/login/` or `/accounts/github/login/`

### JWT API Auth
```bash
# Get JWT token
POST /api/token/
{"username": "user", "password": "pass"}

# Use token in requests
curl -H "Authorization: Bearer <access_token>" /api/projects/
```

### OAuth Setup
1. Go to Google Cloud Console → Create OAuth 2.0 credentials
2. Redirect URI: `http://localhost:8000/accounts/google/login/callback/`
3. Add `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` to env

Same for GitHub at github.com/settings/developers.

Then in Django admin → Sites → add `localhost:8000`
And Social Applications → add your credentials.

## 📊 Admin Panel

Visit `/admin/` with your superuser credentials to manage:
- **Profile** — name, bio, images, social links, CV
- **Skills** — name, icon, category, proficiency bar
- **Education & Experience** — timeline entries
- **Projects** — with images, tech tags, links
- **Contact Messages** — view, mark as read/replied
- **Users** — manage accounts

## 🌐 API Endpoints

| Endpoint | Auth | Description |
|----------|------|-------------|
| `GET /api/profile/` | Public | Profile info |
| `GET /api/skills/` | Public | Skills list |
| `GET /api/projects/` | JWT | Projects list |
| `GET /api/projects/<id>/` | JWT | Project detail |
| `POST /api/contact/` | JWT | Send message |
| `POST /api/token/` | None | Get JWT tokens |
| `POST /api/token/refresh/` | None | Refresh token |

## 🎨 Customization

1. **Profile**: Django admin → Portfolio → Profiles
2. **Colors**: Edit CSS variables in `static/css/main.css` (`:root` block)
3. **Add skills**: Django admin → Portfolio → Skills
4. **Upload CV**: Django admin → Profile → CV file field

## 🚢 Production Deployment

```bash
# Set environment variables
export DEBUG=False
export SECRET_KEY=<strong-random-key>
export ALLOWED_HOSTS=yourdomain.com

# Use Gunicorn
gunicorn portfolio_project.wsgi:application --bind 0.0.0.0:8000

# Or with Nginx + Gunicorn (recommended)
```
