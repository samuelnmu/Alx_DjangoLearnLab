from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Library

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
# Role check helper functions
# ===============================
def is_admin(user):
    """
    Returns True if the logged-in user has a related UserProfile
    and their role is 'Admin'.
    hasattr(user, 'userprofile') ensures we don't get an AttributeError
    if the user does not have a profile.
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
# The @ symbol in Python is used for decorators.
# A decorator modifies the behavior of a function or method.
# In this case, @user_passes_test ensures that only users
# who pass the given test function can access the view.

@user_passes_test(is_admin)  # Only allow users where is_admin(user) returns True
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
