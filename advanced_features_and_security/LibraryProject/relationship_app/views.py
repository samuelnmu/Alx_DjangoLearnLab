from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .models import Book, Library
from .forms import BookForm  # Ensure you have a form for Book


# ===============================
# Function-based view: List all books
# ===============================
def list_books(request):
    """
    Retrieves all Book objects from the database and
    renders them in the list_books.html template.
    """
    books = Book.objects.all()  # Fetch all books from the database
    return render(request, 'relationship_app/list_books.html', {'books': books})


# ===============================
# Class-based view: Library detail
# ===============================
class LibraryDetailView(DetailView):
    """
    Displays details for a single Library object.
    The object is fetched based on the primary key (pk) from the URL.
    """
    model = Library  # Model to query
    template_name = 'relationship_app/library_detail.html'  # Template to render
    context_object_name = 'library'  # Template variable name for the object


# ===============================
# Permission-protected CRUD views for Book
# ===============================

@permission_required('relationship_app.can_add_book')
def add_book(request):
    """Allows adding a new book (requires can_add_book permission)."""
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    """Allows editing an existing book (requires can_change_book permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    """Allows deleting a book (requires can_delete_book permission)."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list-books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})


# ===============================
# Role check helper functions
# ===============================
def is_admin(user):
    """
    Returns True if the logged-in user has a related UserProfile
    and their role is 'Admin'.
    """
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    """Check if user is a Librarian."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    """Check if user is a Member."""
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# ===============================
# Role-restricted views
# ===============================
@user_passes_test(is_admin)  # Only allow Admin users
def admin_view(request):
    """View accessible only to Admin role."""
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)  # Only allow Librarians
def librarian_view(request):
    """View accessible only to Librarian role."""
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)  # Only allow Members
def member_view(request):
    """View accessible only to Member role."""
    return render(request, 'relationship_app/member_view.html')
