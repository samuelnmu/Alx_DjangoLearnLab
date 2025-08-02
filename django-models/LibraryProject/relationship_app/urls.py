from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list-books'),

    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
