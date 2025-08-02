from relationship_app.models import Author, Book, Library, Librarian

def query_books():
    """Query 1: All books by a specific author"""
    author_name = "J.K. Rowling"
    try:
        # Filter books directly by author name using double underscores
        books_by_author = Book.objects.filter(author__name=author_name)
        if books_by_author.exists():
            print(f"Books by {author_name}:")
            for book in books_by_author:
                print(f" - {book.title}")
        else:
            print(f"No books found by {author_name}")
    except Exception as e:
        print(f"Error: {e}")


def query_lib_books():
    """Query 2: All books in a specific library"""
    library_name = "Central Library"
    try:
        # Filter books via library relationship
        books_in_library = Book.objects.filter(library__name=library_name)
        if books_in_library.exists():
            print(f"\nBooks in {library_name}:")
            for book in books_in_library:
                print(f" - {book.title} (by {book.author.name})")
        else:
            print(f"No books found in {library_name}")
    except Exception as e:
        print(f"Error: {e}")


def query_librarian():
    """Query 3: Librarian of a library"""
    library_name = "Central Library"
    try:
        # Get librarian via library name
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"\nLibrarian of {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for library: {library_name}")
