from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json

from .models import Author, Book

# Dynamically get the User model (works with both default and custom models)
User = get_user_model()


class BookAPITests(APITestCase):
    """
    Comprehensive test suite for Book API endpoints.

    Key Notes:
    - Uses APITestCase → sets up an isolated test DB that is reset after tests.
    - self.client is a DRF APIClient → simulates HTTP requests without starting a server.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Called ONCE for the test class (faster than per-test `setUp` for large data).

        Under the hood:
        - Creates test users in the database.
        - Creates authors and books for testing.
        - Precomputes frequently-used endpoint URLs.
        """
        # Create test users
        cls.user = User.objects.create_user(username="alice", password="password123")
        cls.other_user = User.objects.create_user(username="bob", password="password123")

        # Create authors
        cls.a_rowling = Author.objects.create(name="J. K. Rowling")
        cls.a_tolkein = Author.objects.create(name="J. R. R. Tolkien")  # note misspelling for test consistency
        cls.a_him = Author.objects.create(name="Himothy Green")

        # Create books
        cls.b1 = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=cls.a_rowling
        )
        cls.b2 = Book.objects.create(
            title="Harry Potter and the Chamber of Secrets",
            publication_year=1998,
            author=cls.a_rowling
        )
        cls.b3 = Book.objects.create(
            title="The Hobbit",
            publication_year=1937,
            author=cls.a_tolkein
        )
        cls.b4 = Book.objects.create(
            title="Himothy Memoir",
            publication_year=2010,
            author=cls.a_him
        )

        # Store endpoint URLs
        cls.url_list = reverse("book-list")     # GET all books
        cls.url_create = reverse("book-create") # POST new book

    def setUp(self):
        """
        Called before each test method.

        Under the hood:
        - Creates a fresh APIClient so that authentication state doesn’t leak between tests.
        """
        self.client = APIClient()

    def get_json(self, resp):
        """
        Helper method to decode a DRF Response object into a Python dict/list.
        This avoids using `response.data` directly.
        """
        return json.loads(resp.content)

    # ---------- LIST / RETRIEVE ----------
    def test_list_books_public_access(self):
        """Anyone can list all books without authentication."""
        resp = self.client.get(self.url_list)
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(data), 4)
        titles = [b["title"] for b in data]
        self.assertIn(self.b3.title, titles)

    def test_retrieve_book_public_access(self):
        """Anyone can retrieve a single book by its ID."""
        url = reverse("book-detail", kwargs={"pk": self.b3.pk})
        resp = self.client.get(url)
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.b3.title)
        self.assertEqual(data["publication_year"], self.b3.publication_year)

    # ---------- CREATE ----------
    def test_create_book_requires_auth(self):
        """Unauthenticated users cannot create books (expect 401)."""
        payload = {"title": "New Book", "publication_year": 2020, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users can create books."""
        self.client.force_authenticate(user=self.user)  # bypasses login flow
        payload = {"title": "Clean Code in Django", "publication_year": 2021, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["publication_year"], payload["publication_year"])
        self.assertIn("message", data)  # check for custom success message

    def test_create_book_future_year_rejected(self):
        """Creating a book with a future year should fail validation."""
        self.client.force_authenticate(user=self.user)
        payload = {"title": "From The Future", "publication_year": 3000, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- UPDATE ----------
    def test_update_book_requires_auth(self):
        """Unauthenticated users cannot update books."""
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "HP1 (Edited)", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Authenticated users can update books."""
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "HP1 (Edited)", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "HP1 (Edited)")
        self.assertIn("message", data)

    def test_update_book_empty_title_rejected(self):
        """Updating a book with an empty title should fail."""
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- DELETE ----------
    def test_delete_book_requires_auth(self):
        """Unauthenticated users cannot delete books."""
        url = reverse("book-delete", kwargs={"pk": self.b2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        """Authenticated users can delete books."""
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", kwargs={"pk": self.b2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.b2.pk).exists())

    # ---------- FILTERING ----------
    def test_filter_by_title_exact(self):
        """Filter books by exact title."""
        resp = self.client.get(self.url_list, {"title": "The Hobbit"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "The Hobbit")

    def test_filter_by_author_fk_id(self):
        """Filter books by author ID."""
        resp = self.client.get(self.url_list, {"author": self.a_rowling.pk})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned_authors = {item["author"] for item in data}
        self.assertTrue(all(a_id == self.a_rowling.pk for a_id in returned_authors))

    def test_filter_by_publication_year(self):
        """Filter books by publication year."""
        resp = self.client.get(self.url_list, {"publication_year": 1937})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "The Hobbit")

    # ---------- SEARCH ----------
    def test_search_by_title_icontains(self):
        """Search books by partial title match (case-insensitive)."""
        resp = self.client.get(self.url_list, {"search": "harry"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"].lower() for b in data]
        self.assertTrue(any("harry potter" in t for t in titles))

    # ---------- ORDERING ----------
    def test_order_by_title_asc(self):
        """Order books by title ascending."""
        resp = self.client.get(self.url_list, {"ordering": "title"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in data]
        self.assertEqual(titles, sorted(titles))

    def test_order_by_publication_year_desc(self):
        """Order books by publication year descending."""
        resp = self.client.get(self.url_list, {"ordering": "-publication_year"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in data]
        self.assertEqual(years, sorted(years, reverse=True))
