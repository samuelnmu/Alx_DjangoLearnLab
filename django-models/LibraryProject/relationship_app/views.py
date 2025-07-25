# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Library  # <-- Exact match for "from .models import Library"
from django.views.generic.detail import DetailView

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
