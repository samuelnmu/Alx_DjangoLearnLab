# relationship_app/urls.py

from django.urls import path
from .views import (
    list_books,
    LibraryDetailView,
    register_view,
    CustomLoginView,
    CustomLogoutView,
)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Auth URLs
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
