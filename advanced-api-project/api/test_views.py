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
        Prepare environment before each test:
        - Create a test user
        - Create sample Author & Book
        - Log in via `self.client.login()` (instead of force_authenticate)
        """
        # Create test user
        self.user_password = "pass1234"
        self.user = User.objects.create_user(username="testuser", password=self.user_password)

        # Create sample Author & Book
        self.author = Author.objects.create(name="John Doe")
        self.book = Book.objects.create(title="Sample Book", author=self.author)

        # Log in using Django's test client (sets session)
        self.client.login(username="testuser", password=self.user_password)

    def get_json(self, response):
        """
        Helper to parse JSON from response.content (avoids using response.data)
        """
        return json.loads(response.content)

    # ---------- LIST ----------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data[0]["title"], "Sample Book")

    # ---------- CREATE ----------
    def test_create_book(self):
        url = reverse("book-list")
        payload = {"title": "New Book", "author": self.author.id}
        response = self.client.post(url, payload, format="json")
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], "New Book")

    # ---------- RETRIEVE ----------
    def test_retrieve_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.get(url)
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Sample Book")

    # ---------- UPDATE ----------
    def test_update_book(self):
        url = reverse("book-detail", args=[self.book.id])
        payload = {"title": "Updated Book", "author": self.author.id}
        response = self.client.put(url, payload, format="json")
        data = self.get_json(response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Updated Book")

    # ---------- DELETE ----------
    def test_delete_book(self):
        url = reverse("book-detail", args=[self.book.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
