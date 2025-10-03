# Blog Post Management

## Features
- **List posts** (`/`) → view all posts.
- **Detail view** (`/posts/<id>/`) → view a single post.
- **Create post** (`/posts/new/`) → logged-in users can create posts.
- **Update post** (`/posts/<id>/edit/`) → only the author can edit.
- **Delete post** (`/posts/<id>/delete/`) → only the author can delete.

## Permissions
- Guests: can view list & details.
- Logged-in users: can create posts.
- Authors: can edit/delete their own posts.

## Notes
- Posts automatically set the logged-in user as author.
- Posts ordered by latest published date.
