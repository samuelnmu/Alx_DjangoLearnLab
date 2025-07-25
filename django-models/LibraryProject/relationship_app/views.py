# relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from .models import Book
from .models import Library  # <-- Exact match for "from .models import Library"
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('list_books')  # Redirect to book list or home page
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def check_role(role):
    def inner(user):
        return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == role
    return user_passes_test(inner)

@login_required
@check_role('Admin')
def admin_view(request):
    return render(request, 'admin_view.html')

@login_required
@check_role('Librarian')
def librarian_view(request):
    return render(request, 'librarian_view.html')

@login_required
@check_role('Member')
def member_view(request):
    return render(request, 'member_view.html')
