Advanced API Project
This project demonstrates building a Django REST Framework API with:

Custom serializers (nested relationships & validation)
Generic views (CRUD for books)
Permissions (read-only for public, write for authenticated users)
API Endpoints
Books
GET /api/books/ → List all books (public)
GET /api/books/<id>/ → Retrieve book by ID (public)
POST /api/books/create/ → Create a new book (authenticated only)
PUT /api/books/<id>/update/ → Update a book (authenticated only)
DELETE /api/books/<id>/delete/ → Delete a book (authenticated only)
Permissions
Read: Open to everyone
Write (create/update/delete): Requires authentication
Testing
Use the Django admin panel to add authors/books.
Use Postman or curl to test the endpoints.
Example:
curl -X GET http://127.0.0.1:8000/api/books/
Filtering, Searching, and Ordering
The Books API supports advanced query options:

Filtering
/api/books/?title=Things Fall Apart
/api/books/?publication_year=1960
/api/books/?author=1
Searching
/api/books/?search=Chinua
/api/books/?search=Fall
Ordering
/api/books/?ordering=title (A–Z)
/api/books/?ordering=-publication_year (Newest first)
