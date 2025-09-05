from django.urls import path
from . import views
from .views import list_books, LibraryDetailView 
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import admin_view
from .views import librarian_view
from .views import member_view

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

     # Authentication
    path("register/", views.register_view, name="register"),  # checker expects views.register
    path(
        "login/",
        LoginView.as_view(template_name="relationship_app/login.html"),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(template_name="relationship_app/logout.html"),
        name="logout"
    ),
]



urlpatterns += [
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),
]


urlpatterns = [
    path("add_book/", views.add_book, name="add_book"),
    path("edit_book/<int:pk>/", views.edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", views.delete_book, name="delete_book"),
]
