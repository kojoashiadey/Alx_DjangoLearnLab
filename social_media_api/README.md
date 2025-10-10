# Social Media API

A simple Django REST Framework social media API with user authentication, profiles, follow system, posts feed, likes, and notifications.

## Features

- **Custom User Model** with bio, profile picture, and followers system
- **Token Authentication** using DRF authtoken
- **User Registration & Login**
- **Follow/Unfollow System**
- **Post Feed** with pagination
- **Like/Unlike Posts**
- **Notifications** system

## Setup

### Prerequisites
- Python 3.x
- Virtualenv

### Installation

1. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure settings in `settings.py`:**
```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',  # your accounts app
]

AUTH_USER_MODEL = "accounts.User"

# For profile pictures (development)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

4. **Run migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create superuser:**
```bash
python manage.py createsuperuser
```

6. **Run development server:**
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

- **POST** `/api/accounts/register/` - Register new user (returns token + user data)
- **POST** `/api/accounts/login/` - Login user (returns token + user data)

### User Profiles

- **GET** `/api/accounts/profile/<user_id>/` - Get public user profile
- **GET/PUT** `/api/accounts/me/` - Retrieve/update authenticated user's profile

### Follow System

- **POST** `/api/accounts/follow/<user_id>/` - Follow a user (auth required)
- **POST** `/api/accounts/unfollow/<user_id>/` - Unfollow a user (auth required)
- **GET** `/api/accounts/following/` - List users you follow (auth required)
- **GET** `/api/accounts/followers/` - List users following you (auth required)

### Feed

- **GET** `/api/feed/` - Get paginated posts from users you follow (auth required)
  - Query parameters: `page`, `page_size`

### Likes

- **POST** `/api/posts/<post_id>/like/` - Like a post (auth required)
  - Returns `201 Created` with Like object on success
  - Returns `400` if already liked
- **POST** `/api/posts/<post_id>/unlike/` - Unlike a post (auth required)
  - Returns `201 Created` on success
  - Returns `400` if not liked

### Notifications

- **GET** `/api/notifications/` - List recipient's notifications (auth required)
- **PATCH** `/api/notifications/<notification_id>/read/` - Mark a single notification as read
- **POST** `/api/notifications/mark-all-read/` - Mark all unread notifications as read

## Important Notes

- **Set `AUTH_USER_MODEL` before running initial migrations**
- For profile pictures in development, ensure `DEBUG=True` and `MEDIA_URL`/`MEDIA_ROOT` are properly configured
- All endpoints except registration and login require authentication via token

## Authentication

Include the token in request headers:
```
Authorization: Token <your_token>
```
