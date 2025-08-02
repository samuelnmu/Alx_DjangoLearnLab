from django.urls import path
from .views import list_books, LibraryDetailView
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list-books'),

    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    
    
    path('admin-only/', admin_view, name='admin-view'),
    path('librarian-only/', librarian_view, name='librarian-view'),
    path('member-only/', member_view, name='member-view'),
]
