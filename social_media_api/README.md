social_media_api (Alx_DjangoLearnLab)
Overview
Simple Social Media API starter with:

Custom user model (bio, profile_picture, followers)
Token authentication (DRF rest_framework.authtoken)
Registration, login, user profile, follow/unfollow endpoints
Setup
Create & activate virtualenv
Install deps: pip install -r requirements.txt
Ensure settings.py contains:
INSTALLED_APPS includes 'rest_framework', 'rest_framework.authtoken', 'accounts'
AUTH_USER_MODEL = "accounts.User"
MEDIA_URL / MEDIA_ROOT set for profile pictures
Make migrations & migrate: python manage.py makemigrations python manage.py migrate
Create superuser: python manage.py createsuperuser
Run server: python manage.py runserver
Endpoints
POST /api/accounts/register/ → register; returns token + user
POST /api/accounts/login/ → login; returns token + user
GET /api/accounts/profile// → public profile
GET/PUT /api/accounts/me/ → retrieve/update authenticated user's profile
POST /api/accounts/follow// → follow/unfollow toggle
Notes
Important: set AUTH_USER_MODEL before initial migrations.
To use profile pictures in development, ensure DEBUG=True and MEDIA_URL/MEDIA_ROOT configured.
Follows
POST /api/accounts/follow/<user_id>/ — Follow a user (auth required) POST /api/accounts/unfollow/<user_id>/ — Unfollow a user (auth required) GET /api/accounts/following/ — List users you follow (auth required) GET /api/accounts/followers/ — List users following you (auth required)

Feed
GET /api/feed/ — Get paginated posts from users you follow (auth required) Query params: page, page_size

Likes
POST /api/posts//like/ — like a post (auth required) POST /api/posts//unlike/ — unlike a post (auth required)

Responses:

201 Created with Like object on success
400 if already liked / not liked
Notifications
GET /api/notifications/ — list recipient's notifications (auth) PATCH /api/notifications//read/ — mark a single notification read POST /api/notifications/mark-all-read/ — mark all unread notifications as read
