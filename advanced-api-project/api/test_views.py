from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
import json

from .models import Author, Book

# Dynamically get the User model (supports custom user models)
User = get_user_model()


class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.
    Uses Django REST Framework's APITestCase, which sets up:
    - An isolated test database
    - A test client (`self.client`) for simulating HTTP requests
    """

    @classmethod
    def setUpTestData(cls):
        """Called once for the entire test class."""
        cls.user = User.objects.create_user(username="alice", password="password123")
        cls.other_user = User.objects.create_user(username="bob", password="password123")

        cls.a_rowling = Author.objects.create(name="J. K. Rowling")
        cls.a_tolkein = Author.objects.create(name="J. R. R. Tolkien")
        cls.a_him = Author.objects.create(name="Himothy Green")

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

        cls.url_list = reverse("book-list")
        cls.url_create = reverse("book-create")

    def setUp(self):
        """Runs before each test."""
        self.client = APIClient()

    def get_json(self, resp):
        """Helper to load JSON from response without using `response.data`."""
        return json.loads(resp.content)

    # ---------- LIST / RETRIEVE ----------
    def test_list_books_public_access(self):
        resp = self.client.get(self.url_list)
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(data), 4)
        titles = [b["title"] for b in data]
        self.assertIn(self.b3.title, titles)

    def test_retrieve_book_public_access(self):
        url = reverse("book-detail", kwargs={"pk": self.b3.pk})
        resp = self.client.get(url)
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.b3.title)
        self.assertEqual(data["publication_year"], self.b3.publication_year)

    # ---------- CREATE ----------
    def test_create_book_requires_auth(self):
        payload = {"title": "New Book", "publication_year": 2020, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Clean Code in Django", "publication_year": 2021, "author": self.a_rowling.pk}
        resp = self.client.post(self.url_create, payload, format="json")
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["publication_year"], payload["publication_year"])
        self.assertIn("message", data)

    def test_create_book_future_year_rejected(self):
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
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "HP1 (Edited)")
        self.assertIn("message", data)

    def test_update_book_empty_title_rejected(self):
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
        self.assertFalse(Book.objects.filter(pk=self.b2.pk).exists())

    # ---------- FILTERING ----------
    def test_filter_by_title_exact(self):
        resp = self.client.get(self.url_list, {"title": "The Hobbit"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "The Hobbit")

    def test_filter_by_author_fk_id(self):
        resp = self.client.get(self.url_list, {"author": self.a_rowling.pk})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        returned_authors = {item["author"] for item in data}
        self.assertTrue(all(a_id == self.a_rowling.pk for a_id in returned_authors))

    def test_filter_by_publication_year(self):
        resp = self.client.get(self.url_list, {"publication_year": 1937})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "The Hobbit")

    # ---------- SEARCH ----------
    def test_search_by_title_icontains(self):
        resp = self.client.get(self.url_list, {"search": "harry"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"].lower() for b in data]
        self.assertTrue(any("harry potter" in t for t in titles))

    # ---------- ORDERING ----------
    def test_order_by_title_asc(self):
        resp = self.client.get(self.url_list, {"ordering": "title"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in data]
        self.assertEqual(titles, sorted(titles))

    def test_order_by_publication_year_desc(self):
        resp = self.client.get(self.url_list, {"ordering": "-publication_year"})
        data = self.get_json(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in data]
        self.assertEqual(years, sorted(years, reverse=True))
