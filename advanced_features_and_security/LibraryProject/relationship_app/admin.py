from django.contrib import admin
from .models import Book, Library, Library_books, Librarian, UserProfile

admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Library_books)
admin.site.register(Librarian)
admin.site.register(UserProfile)
