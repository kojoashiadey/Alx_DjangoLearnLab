User Authentication System Documentation
Overview

The authentication system in the Django Blog project enables users to:

Register a new account

Log in to their account

Log out securely

View their profile information

This system is built using Django’s built-in authentication framework, extended with a custom registration form and profile view.

Features

User Registration

New users can sign up with a username, email, and password.

Passwords are hashed securely by Django before being stored in the database.

Upon successful registration, users are automatically logged in and redirected to their profile page.

User Login

Existing users can log in using their username and password.

Invalid login attempts display error messages for user guidance.

User Logout

Logged-in users can log out securely.

After logout, users are redirected to a confirmation page with the option to log back in.

User Profile

Authenticated users can view their profile details (username and email).

The profile page is protected and requires the user to be logged in.

Routes (URLs)
Path	View	Description
/register/	register	Register a new account
/login/	CustomLoginView	Log in with username & password
/logout/	CustomLogoutView	Log out from the system
/profile/	profile	View user profile (login required)
Templates

register.html → Registration form

login.html → Login form

logout.html → Logout confirmation page

profile.html → Profile details page

All templates extend from the base layout (base.html) and use Django’s form rendering system.

Security

CSRF Protection: All forms include {% csrf_token %} to prevent CSRF attacks.

Password Hashing: Passwords are securely hashed using Django’s built-in authentication system.

Access Control: The profile page is restricted to logged-in users only via the @login_required decorator.

How to Test

Registration

Navigate to /register/

Enter username, email, and password → confirm registration

Verify you are redirected to your profile page

Login

Navigate to /login/

Enter credentials for an existing user

Verify redirection to profile page

Logout

Click logout button or go to /logout/

Verify the logout confirmation page is displayed

Profile

Navigate to /profile/

Ensure only logged-in users can access it (non-logged-in users should be redirected to login page)
