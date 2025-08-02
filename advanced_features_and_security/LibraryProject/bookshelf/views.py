from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from django.db.models import Q

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

# View Books — requires can_view
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure book listing with optional search.
    Uses Django ORM filtering to avoid SQL injection.
    """
    query = request.GET.get('q', '')
    if query:
        # Using ORM filters to prevent SQL injection
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()

    return render(request, 'bookshelf/book_list.html', {'books': books, 'query': query})

# Add Book — requires can_create
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Edit Book — requires can_edit
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list-books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Delete Book — requires can_delete
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list-books')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})
