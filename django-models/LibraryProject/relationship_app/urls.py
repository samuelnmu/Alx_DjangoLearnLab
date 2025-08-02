from django.urls import path
from .views import list_books, LibraryDetailView, admin_view, librarian_view, member_view

# URL patterns for relationship_app
urlpatterns = [
    # Function-based view: List all books in the database
    path('books/', list_books, name='list-books'),

    # Class-based view: Display details for a specific library (identified by primary key <pk>)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),

    # Function-based view: Accessible only to Admin role
    path('admin-only/', admin_view, name='admin-view'),

    # Function-based view: Accessible only to Librarian role
    path('librarian-only/', librarian_view, name='librarian-view'),

    # Function-based view: Accessible only to Member role
    path('member-only/', member_view, name='member-view'),
]
