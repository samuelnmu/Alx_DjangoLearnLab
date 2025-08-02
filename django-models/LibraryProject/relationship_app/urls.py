from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    admin_view,
    librarian_view,
    member_view,
    add_book,
    edit_book,
    delete_book
)

# URL patterns for relationship_app
urlpatterns = [
    # ===============================
    # Function-based view: List all books in the database
    # ===============================
    path('books/', list_books, name='list-books'),

    # ===============================
    # Class-based view: Display details for a specific library (identified by primary key <pk>)
    # ===============================
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),

    # ===============================
    # Permission-protected CRUD views for Book
    # ===============================
    path('books/add/', add_book, name='add-book'),          # Requires can_add_book
    path('books/<int:pk>/edit/', edit_book, name='edit-book'),   # Requires can_change_book
    path('books/<int:pk>/delete/', delete_book, name='delete-book'), # Requires can_delete_book

    # ===============================
    # Role-based access views
    # ===============================
    path('admin-only/', admin_view, name='admin-view'),         # Accessible only to Admin role
    path('librarian-only/', librarian_view, name='librarian-view'), # Accessible only to Librarian role
    path('member-only/', member_view, name='member-view'),      # Accessible only to Member role
]
