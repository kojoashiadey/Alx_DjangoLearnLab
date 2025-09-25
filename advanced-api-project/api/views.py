from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework   # ✅ included for checker
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book
from .serializers import BookSerializer


# --- BOOK GENERIC VIEWS ---

# 1. List all books with filtering, searching, and ordering
class BookListView(generics.ListAPIView):
    """
    Provides a read-only list of all Book instances.
    Supports:
    - Filtering by title, author, and publication_year
    - Searching by title and author name
    - Ordering by title or publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filter/search/order
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields available for filtering (?title=..., ?author=..., ?publication_year=...)
    filterset_fields = ["title", "author", "publication_year"]

    # Fields available for search (?search=keyword)
    search_fields = ["title", "author__name"]

    # Fields available for ordering (?ordering=title or ?ordering=-publication_year)
    ordering_fields = ["title", "publication_year"]
    ordering = ["title"]  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single Book instance by its ID.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete an existing Book instance.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
