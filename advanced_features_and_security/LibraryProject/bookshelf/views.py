from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from .models import Book
from .forms import BookForm
from .forms import ExampleForm

"""
PERMISSIONS & GROUPS SETUP GUIDE:

Custom Permissions (in Book model):
    - can_view: View books
    - can_create: Add new books
    - can_edit: Edit existing books
    - can_delete: Delete books

Groups (to be created in Django Admin):
    - Viewers: can_view
    - Editors: can_view, can_create, can_edit
    - Admins: can_view, can_create, can_edit, can_delete

Usage:
    - Assign permissions to groups in Django Admin.
    - Assign users to groups.
    - The @permission_required decorator in views enforces these permissions.
"""

# ===============================
# View Books — requires can_view
# ===============================
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure book listing with optional search.
    Uses Django ORM filtering to avoid SQL injection.
    """
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})


# ===============================
# Add Book — requires can_create
# ===============================
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')  # ✅ use consistent name
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ===============================
# Edit Book — requires can_edit
# ===============================
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book-list')  # ✅ use consistent name
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})


# ===============================
# Delete Book — requires can_delete
# ===============================
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book-list')  # ✅ use consistent name
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


# ===============================
# Example Form View — demonstrates CSRF and safe form handling
# ===============================
def example_form_view(request):
    """
    Demonstrates using ExampleForm with CSRF protection
    and safe data handling.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Here you can safely process the data
            return render(request, 'bookshelf/form_success.html', {'name': name})
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})
