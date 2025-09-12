📌 retrieve.md
# Retrieve Book Test

```python
from bookshelf.models import Book

# Retrieve the book
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year
Expected Output
text
Copy
Edit
('1984', 'George Orwell', 1949)
