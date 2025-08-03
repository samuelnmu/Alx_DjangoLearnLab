from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, permissions

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Read allowed for anyone, write allowed for admins only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff

class BookViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    for listing, creating, retrieving, updating, and deleting Books.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly] 
    
