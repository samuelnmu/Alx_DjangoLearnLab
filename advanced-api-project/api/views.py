from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView,RetrieveAPIView, DestroyAPIView
from .models import Book
from .serializers import BookSerializer
from rest_framework import permissions
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework import generics



#List all books
class BookListView(ListAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    # permission_classes=[IsAuthenticatedOrReadOnly]
    
    #Filter backends
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Filtering
    filterset_fields = ['title', 'author', 'publication_year']
    # Searching
    search_fields = ['title', 'author']
    # Ordering
    ordering_fields = ['title', 'publication_year']

#Create a new book  
class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can create

    def perform_create(self, serializer):
        """
        This method is called after validation but before saving.
        You can customize creation logic here.
        """
        # Example: prevent future publication years at view level (extra layer)
        if serializer.validated_data['publication_year'] > 2025:
            raise serializers.ValidationError("Cannot create a book with a future publication year.")

        # Save the instance
        serializer.save()

    def create(self, request, *args, **kwargs):
        """
        Override to customize the response after creation
        """
        response = super().create(request, *args, **kwargs)
        response.data['message'] = "Book successfully created!"
        return response

#Update an existing book    
class BookUpdateView(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Called before saving an updated instance
        """
        # Example: prevent updating title to empty string
        if serializer.validated_data.get('title', '') == '':
            raise serializers.ValidationError("Title cannot be empty.")
        serializer.save()

    def update(self, request, *args, **kwargs):
        """
        Customize response after update
        """
        response = super().update(request, *args, **kwargs)
        response.data['message'] = "Book successfully updated!"
        return response
    
#Retrieve a single book by ID (pk)
class BookDetailView(RetrieveAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
#Delete a book
class BookDeleteView(DestroyAPIView):
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticated]