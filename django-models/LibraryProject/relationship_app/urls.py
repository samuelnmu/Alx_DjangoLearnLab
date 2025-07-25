from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Register
    path('register/', views.register, name='register'),

    # Login
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),

    # Logout
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
]
