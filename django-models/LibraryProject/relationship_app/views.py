from .models import Book, Library
from django.views.generic.detail import DetailView
from django.shortcuts import render
#lists all books stored in the database.

# Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

#display details for a specific library, listing all books available in that library.

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'  # Template file
    context_object_name = 'library'  # The name used in the template

