from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

# Dynamically get the User model (supports custom user models)
User = get_user_model()


class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.

    Uses Django REST Framework's APITestCase, which sets up:
    - An isolated test database (rolled back after tests)
    - A test client (`self.client`) that simulates HTTP requests
    """

    @classmethod
    def setUpTestData(cls):
        """
        Called once for the entire test class (faster than setUp for heavy fixtures).
        Creates initial test data for all tests to share.
        """
        # Create two test users
        cls.user = User.objects.create_user(username="alice", password="password123")
        cls.other_user = User.objects.create_user(username="bob", password="password123")

        # Create authors
        cls.a_rowling = Author.objects.create(name="J. K. Rowling")
        cls.a_tolkein = Author.objects.create(name="J. R. R. Tolkien")  # misspelling kept for test consistency
        cls.a_him = Author.objects.create(name="Himothy Green")

        # Create books linked to authors
        cls.b1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=cls.a_rowling)
        cls.b2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", publication_year=1998, author=cls.a_rowling)
        cls.b3 = Book.objects.create(title="The Hobbit", publication_year=1937, author=cls.a_tolkein)
        cls.b4 = Book.objects.create(title="Himothy Memoir", publication_year=2010, author=cls.a_him)

        # Store common endpoint URLs for reuse
        cls.url_list = reverse("book-list")     # GET list of books
        cls.url_create = reverse("book-create") # POST create a new book

    def setUp(self):
        """
        Runs before each test method.
        Creates a fresh APIClient instance for isolation.
        """
        self.client = APIClient()

    # ---------- LIST / RETRIEVE ----------
    def test_list_books_public_access(self):
        # Anyone can list books (no auth required)
        resp = self.client.get(self.url_list)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 4)
        titles = [b["title"] for b in resp.data]
        self.assertIn(self.b3.title, titles)

    def test_retrieve_book_public_access(self):
        # Anyone can retrieve a single book by ID
        url = reverse("book-detail", kwargs={"pk": self.b3.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # Validate response body content
        self.assertEqual(resp.data["title"], self.b3.title)
        self.assertEqual(resp.data["publication_year"], self.b3.publication_year)

    # ---------- CREATE ----------
    def test_create_book_requires_auth(self):
        # Unauthenticated users get 401 Unauthorized
        payload = {"title": "New Book", "publication_year": 2020, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        # Authenticated user can create a book
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Clean Code in Django", "publication_year": 2021, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], payload["title"])
        self.assertEqual(resp.data["publication_year"], payload["publication_year"])
        # Custom success message from view
        self.assertIn("message", resp.data)

    def test_create_book_future_year_rejected(self):
        # Creating with a year beyond current_year is blocked (view or model validation)
        self.client.force_authenticate(user=self.user)
        payload = {"title": "From The Future", "publication_year": 3000, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- UPDATE ----------
    def test_update_book_requires_auth(self):
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "HP1 (Edited)", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "HP1 (Edited)", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "HP1 (Edited)")
        self.assertIn("message", resp.data)

    def test_update_book_empty_title_rejected(self):
        # Validation should reject an empty title
        self.client.force_authenticate(user=self.user)
        url = reverse("book-update", kwargs={"pk": self.b1.pk})
        resp = self.client.put(url, {"title": "", "publication_year": 1997, "author": self.a_rowling.pk}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- DELETE ----------
    def test_delete_book_requires_auth(self):
        url = reverse("book-delete", kwargs={"pk": self.b2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("book-delete", kwargs={"pk": self.b2.pk})
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        # Ensure object is gone from DB
        self.assertFalse(Book.objects.filter(pk=self.b2.pk).exists())

    # ---------- FILTERING ----------
    def test_filter_by_title_exact(self):
        resp = self.client.get(self.url_list, {"title": "The Hobbit"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "The Hobbit")

    def test_filter_by_author_fk_id(self):
        # Filtering by FK expects ID by default
        resp = self.client.get(self.url_list, {"author": self.a_rowling.pk})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned_authors = {item["author"] for item in resp.data}
        self.assertTrue(all(a_id == self.a_rowling.pk for a_id in returned_authors))

    def test_filter_by_publication_year(self):
        resp = self.client.get(self.url_list, {"publication_year": 1937})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["title"], "The Hobbit")

    # ---------- SEARCH ----------
    def test_search_by_title_icontains(self):
        # search_fields=['title','author'] but 'author' FK is not searchable directly by name
        resp = self.client.get(self.url_list, {"search": "harry"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"].lower() for b in resp.data]
        self.assertTrue(any("harry potter" in t for t in titles))

    # ---------- ORDERING ----------
    def test_order_by_title_asc(self):
        resp = self.client.get(self.url_list, {"ordering": "title"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_by_publication_year_desc(self):
        resp = self.client.get(self.url_list, {"ordering": "-publication_year"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.data]
        self.assertEqual(years, sorted(years, reverse=True))
