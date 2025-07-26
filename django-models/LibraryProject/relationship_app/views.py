from django.shortcuts import render, redirect
from django.views.generic import DetailView
from .models import Book
from .models import Library  # ✅ Required literal
from django.views.generic.detail import DetailView  # ✅ Required literal

from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login

# ✅ Function-based view: List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# ✅ Class-based view: Detail of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# ✅ Registration View
class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
        return render(request, 'relationship_app/register.html', {'form': form})

# ✅ Login View
class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# ✅ Logout View
class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
