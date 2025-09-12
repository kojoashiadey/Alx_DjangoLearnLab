# relationship_app/models.py

from django.db import models
from django.conf import settings


class Book(models.Model):
    """A simple Book model to be linked with Library"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_year = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Library(models.Model):
    """Library model that contains many books via a through table"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, through="Library_books", related_name="libraries")

    def __str__(self):
        return self.name


class Library_books(models.Model):
    """Through model for Library and Book relationship"""
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} in {self.library.name}"


class Librarian(models.Model):
    """Librarian assigned to a Library"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    library = models.ForeignKey("relationship_app.Library", on_delete=models.CASCADE, related_name="librarians")

    def __str__(self):
        return f"Librarian: {self.user.username} at {self.library.name}"


class UserProfile(models.Model):
    """Profile extension for CustomUser"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
