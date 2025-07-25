from relationship_app.models import Author, Book, Library, Librarian

def run_queries():
    # Query 1: All books by a specific author
    author_name = "J.K. Rowling"
    try:
        author = Author.objects.get(name=author_name)
        books_by_author = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books_by_author:
            print(f" - {book.title}")
    except Author.DoesNotExist:
        print(f"No author found with name: {author_name}")

    # Query 2: All books in a specific library
    library_name = "Central Library"
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        print(f"\nBooks in {library.name}:")
        for book in books_in_library:
            print(f" - {book.title}")
    except Library.DoesNotExist:
        print(f"No library found with name: {library_name}")

    # Query 3: Librarian of a library
    try:
        librarian = Librarian.objects.get(library__name=library_name)
        print(f"\nLibrarian of {library_name}: {librarian.name}")
    except Librarian.DoesNotExist:
        print(f"No librarian found for library: {library_name}")
