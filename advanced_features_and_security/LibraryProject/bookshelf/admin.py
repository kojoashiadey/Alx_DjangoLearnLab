
from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin



# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ['author', 'publication_year']

class CustomUserAdmin(UserAdmin):
    """Custom admin panel configuration for CustomUser"""
    model = CustomUser
    list_display = ["username", "email", "first_name", "last_name", "is_staff"]


admin.site.register(Book, BookAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
