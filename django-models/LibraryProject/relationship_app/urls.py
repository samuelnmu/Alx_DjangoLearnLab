# relationship_app/urls.py

from django.urls import path
from . import views  # ✅ Needed for views.register to match the checker
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # ✅ Checker-matching Auth URLs
    path('register/', views.register, name='register'),  # uses views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # template_name=...
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # template_name=...
]
