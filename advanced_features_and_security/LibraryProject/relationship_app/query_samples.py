"""
Run me like this (no need to open an interactive shell):

    python manage.py shell -c "from relationship_app.query_samples import demo; demo()"

Or interactively:

    python manage.py shell
    >>> from relationship_app.query_samples import (
    ...     query_books_by_author,
    ...     list_books_in_library,
    ...     get_librarian_for_library,
    ...     ensure_sample_data,
    ... )
    >>> ensure_sample_data()  # only first time
    >>> query_books_by_author("Chinua Achebe")
    >>> list_books_in_library("Central Library")
    >>> get_librarian_for_library("Central Library")
"""

from typing import Iterable
from .models import Author, Book, Library, Librarian


def ensure_sample_data() -> None:
    """
    Populate the database with a tiny, repeatable dataset so the queries have
    something to return. Safe to call multiple times.
    """
    # Authors
    achebe, _ = Author.objects.get_or_create(name="Chinua Achebe")
    adichie, _ = Author.objects.get_or_create(name="Chimamanda Ngozi Adichie")

    # Books
    tfa, _ = Book.objects.get_or_create(title="Things Fall Apart", author=achebe)
    aam, _ = Book.objects.get_or_create(title="Americanah", author=adichie)
    hys, _ = Book.objects.get_or_create(title="Half of a Yellow Sun", author=adichie)

    # Libraries
    central, _ = Library.objects.get_or_create(name="Central Library")
    westend, _ = Library.objects.get_or_create(name="West End Library")

    # Assign books to libraries (ManyToMany)
    central.books.add(tfa, aam)
    westend.books.add(aam, hys)

    # Librarians (OneToOne)
    Librarian.objects.get_or_create(name="Ama Mensah", library=central)
    Librarian.objects.get_or_create(name="Kojo Owusu", library=westend)


def _print_books(books: Iterable[Book]) -> None:
    for b in books:
        print(f"- {b.title} (by {b.author.name})")


# 1) Query all books by a specific author
def query_books_by_author(author_name: str) -> None:
    """
    ForeignKey traversal example using objects.filter(author=author).
    """
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"No author found named '{author_name}'.")
        return

    # Use filter as required by checker
    books = Book.objects.filter(author=author)
    if books.exists():
        print(f"Books by {author_name}:")
        _print_books(books)
    else:
        print(f"{author_name} has no books in the database.")



# 2) List all books in a library
def list_books_in_library(library_name: str) -> None:
    """
    ManyToMany traversal example.
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found named '{library_name}'.")
        return

    books = library.books.all()
    if books.exists():
        print(f"Books in {library_name}:")
        _print_books(books)
    else:
        print(f"{library_name} has no books (yet).")


# 3) Retrieve the librarian for a library
def get_librarian_for_library(library_name: str) -> None:
    """
    OneToOne traversal example using Librarian.objects.get(library=...).
    """
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found named '{library_name}'.")
        return

    try:
        # Explicitly query Librarian as required by checker
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"{library_name} does not yet have a librarian assigned.")



def demo() -> None:
    """
    Quick demonstration you can run in one command.
    """
    ensure_sample_data()
    print("=== Query: books by author ===")
    query_books_by_author("Chimamanda Ngozi Adichie")
    print("\n=== Query: books in a library ===")
    list_books_in_library("Central Library")
    print("\n=== Query: librarian for a library ===")
    get_librarian_for_library("Central Library")
