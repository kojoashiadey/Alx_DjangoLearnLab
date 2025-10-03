# Comment System

## Overview
Users can comment on blog posts. Comments are tied to posts and authors and store timestamps for creation and updates.

## Routes
- Create comment: `post/<post_pk>/comments/new/` (POST)
- Edit comment: `comment/<pk>/update/`
- Delete comment: `comment/<pk>/delete/`

## Permissions
- Only authenticated users may create comments.
- Only the comment author may edit or delete their comment.

## How to use
1. Visit a post's detail page.
2. If logged in, fill the comment box and submit.
3. To edit/delete, click Edit/Delete next to your comment.

## Admin
Comments can also be managed via Django admin if registered.

## Testing
Follow the testing checklist in the README to validate functionality and permissions.
