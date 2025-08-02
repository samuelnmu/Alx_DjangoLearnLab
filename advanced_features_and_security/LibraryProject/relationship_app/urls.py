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

# ===============================
# URL patterns for relationship_app
# ===============================
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
    # Permissions are assigned at the model level in Book.Meta.permissions.
    # Django checks these permissions against the current logged-in user's CustomUser object.
    # ===============================
    path('add_book/', add_book, name='add-book'),               # Requires 'relationship_app.can_add_book'
    path('edit_book/<int:pk>/', edit_book, name='edit-book'),   # Requires 'relationship_app.can_change_book'
    path('delete_book/<int:pk>/', delete_book, name='delete-book'), # Requires 'relationship_app.can_delete_book'

    # ===============================
    # Role-based access views
    # These now use role checks directly from CustomUser.role:
    #   - Admin role → 'Admin'
    #   - Librarian role → 'Librarian'
    #   - Member role → 'Member'
    # Previously, role was stored in UserProfile; now it's a field in CustomUser.
    # ===============================
    path('admin-only/', admin_view, name='admin-view'),           # Accessible only if user.role == 'Admin'
    path('librarian-only/', librarian_view, name='librarian-view'), # Accessible only if user.role == 'Librarian'
    path('member-only/', member_view, name='member-view'),        # Accessible only if user.role == 'Member'
]
