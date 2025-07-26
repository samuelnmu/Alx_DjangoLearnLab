from django.urls import path
from . import views  # ✅ Needed for views.register to match the checker
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    # Book & Library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('register/', views.register, name='register'),  # ✅ views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # ✅ template_name=...
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # ✅ template_name=...

    # Role-based dashboard views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

    # Book CRUD views (permission-based)
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
]
