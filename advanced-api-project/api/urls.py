from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.BookListView.as_view(), name="book-list"),                  # List all books
    path("books/create/", views.BookCreateView.as_view(), name="book-create"),       # Create a book
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),     # Retrieve single book
    path("books/<int:pk>/update/", views.BookUpdateView.as_view(), name="book-update"), # Update book
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name="book-delete"), # Delete book
]
