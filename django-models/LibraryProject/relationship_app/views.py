# relationship_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm  # Import the custom form

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
        form = CustomUserCreationForm(request.POST)  # Use custom form instead of UserCreationForm
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = CustomUserCreationForm()
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