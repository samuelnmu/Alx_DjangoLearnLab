# /api/test_views.py
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
import json

from .models import Author, Book

User = get_user_model()


class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints.
    Uses Django REST Framework's APITestCase for full request/response simulation.
    """

    def setUp(self):
        """
        Prepares the environment before each test:
        - Creates a test user
        - Creates a sample Author and Book
        - Logs in the user via `self.client.login()`
        """
        # Create test user
        self.user_password = "pass1234"
        self.user = User.objects.create_user(username="testuser", password=self.user_password)

        # Create sample Author & Book for testing
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(title="Sample Book", author=self.author)

        # Log in using Django's test client authentication
        # This sends a simulated POST to the login view and sets the session
        self.client.login(username="testuser", password=self.user_password)

    def get_json(self, response):
        """
        Helper method to parse JSON response content into Python dict.
        """
        return json.loads(response.content)

    def test_list_books(self):
        """
        GET /books/ - List all books.
        """
        url = reverse("book-list")
        response = self.client.get(url)
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]["title"], "Sample Book")

    def test_create_book(self):
        """
        POST /books/ - Create a new book.
        """
        url = reverse("book-list")
        payload = {"title": "New Book", "author": self.author.id}
        response = self.client.post(url, payload, format="json")
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], "New Book")

    def test_retrieve_book(self):
        """
        GET /books/{id}/ - Retrieve a book by ID.
        """
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Sample Book")

    def test_update_book(self):
        """
        PUT /books/{id}/ - Update book details.
        """
        url = reverse("book-detail", args=[self.book.id])
        payload = {"title": "Updated Book", "author": self.author.id}
        response = self.client.put(url, payload, format="json")
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Updated Book")

    def test_delete_book(self):
        """
        DELETE /books/{id}/ - Delete a book.
        """
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
