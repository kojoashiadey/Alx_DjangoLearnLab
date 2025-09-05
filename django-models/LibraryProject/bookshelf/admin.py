from django.contrib import admin
from .models import Book

# Register Book with some customization
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # show these fields in list view
    search_fields = ('title', 'author')  # add a search box for title and author
    list_filter = ('publication_year',)  # add filter by publication year
