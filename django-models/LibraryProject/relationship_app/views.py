
from django.shortcuts import render, get_object_or_404
from .models import Book, Library
from django.views.generic.detail import DetailView

# Function-based view
def list_books(request):
    books = Book.objects.select_related('author').all()
    return render(request, 'list_books.html', {'books': books})

# relationship_app/views.py (continued)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

