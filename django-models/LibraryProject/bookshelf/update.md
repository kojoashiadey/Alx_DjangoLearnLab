 update.md
# Update Book Test

```python
from bookshelf.models import Book

# Update the title of the book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book
Expected Output
text
Copy
Edit
<Book: Nineteen Eighty-Four by George Orwell (1949)>
yaml
Copy
Edit
