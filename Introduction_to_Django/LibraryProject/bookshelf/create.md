## Create Operation

```python
from bookshelf.models import Book

# Create a Book instance
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

print(book)
# Output: 1984 by George Orwell (1949)
## Retrieve Operation


from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(book.title)  # Output: 1984
print(book.author)  # Output: George Orwell
print(book.publication_year)  # Output: 1949
## Update Operation


from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

print(book.title)  # Output: Nineteen Eighty-Four
## Delete Operation


from bookshelf.models import Book

book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

print(Book.objects.all())  # Output: <QuerySet []>
