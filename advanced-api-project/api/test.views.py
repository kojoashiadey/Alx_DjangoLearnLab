from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API endpoints.
    Covers CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        
        # Create authors
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        # Create books
        self.book1 = Book.objects.create(
            title="First Book", publication_year=2001, author=self.author1
        )
        self.book2 = Book.objects.create(
            title="Second Book", publication_year=2020, author=self.author2
        )

        # Endpoints
        self.list_url = reverse("book-list")      # /books/
        self.detail_url = reverse("book-detail", args=[self.book1.id])  # /books/<id>/
        self.create_url = reverse("book-create")  # /books/create/
        self.update_url = reverse("book-update", args=[self.book1.id])  # /books/update/<id>/
        self.delete_url = reverse("book-delete", args=[self.book1.id])  # /books/delete/<id>/

    # ---------- READ ----------
    def test_list_books(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Anyone can retrieve a single book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)

    # ---------- CREATE ----------
    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books"""
        data = {"title": "New Book", "publication_year": 2022, "author": self.author1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_create_book_authenticated(self):
        """Authenticated users can create books"""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "New Book", "publication_year": 2022, "author": self.author1.id}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # ---------- UPDATE ----------
    def test_update_book_authenticated(self):
        """Authenticated users can update books"""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Updated Book", "publication_year": 2005, "author": self.author1.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    # ---------- DELETE ----------
    def test_delete_book_authenticated(self):
        """Authenticated users can delete books"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ---------- FILTER, SEARCH, ORDER ----------
    def test_filter_books_by_author(self):
        """Filter books by author"""
        response = self.client.get(self.list_url, {"author": self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "First Book")

    def test_search_books_by_title(self):
        """Search books by title"""
        response = self.client.get(self.list_url, {"search": "Second"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Second Book")

    def test_order_books_by_year_desc(self):
        """Order books by publication_year descending"""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["title"], "Second Book")
