# Tagging & Search

## Tagging
- Tags are simple text labels stored in the `Tag` model.
- When creating or editing a post, use the `tags` input field (comma-separated).
  Example: `django, python, web`
- Tags are created automatically when they don't exist.
- Click a tag link to view all posts with that tag: `/tags/<tag_name>/`.

## Search
- The site search bar (in the header) searches post titles, content, and tag names.
- Search URL: `/search/?q=your+query`
- Results are shown on the search results page; pagination is enabled.

## Notes
- Tags are case-insensitive when searching/creating (will be stored in lowercase).
- For large sites or more advanced features (autocomplete, tag suggestion), consider integrating `django-taggit` or a JS tag input library.
