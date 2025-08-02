from django.urls import path
from .views import LibraryDetailView
from . import views

urlpatterns = [
    #function based views
    path('books/',views.list_books,name='list-books'),
    #class based views
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]
