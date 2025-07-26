# relationship_app/query_samples.py
from relationship_app.models import Author, Book, Library, Librarian

def get_books_by_author(author_name):
    """Query all books by a specific author using objects.filter()"""
    try:
        author = Author.objects.get(name=author_name)
        # Using objects.filter(author=author) as requested
        books = Book.objects.filter(author=author)
        print(f"Books by {author_name} (using filter):")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def get_books_by_author_related_name(author_name):
    """Alternative: Query all books by a specific author using related_name"""
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using the related_name 'books'
        print(f"Books by {author_name} (using related_name):")
        for book in books:
            print(f"- {book.title}")
        return books
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return []

def get_books_in_library(library_name):
    """List all books in a library"""
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library_name} library:")
        for book in books:
            print(f"- {book.title} (by {book.author.name})")
        return books
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return []

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library"""
    try:
        library = Library.objects.get(name=library_name)
        try:
            librarian = library.librarian  # Using the related_name 'librarian'
            print(f"Librarian for {library_name}: {librarian.name}")
            return librarian
        except Librarian.DoesNotExist:
            print(f"No librarian assigned to {library_name}")
            return None
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None

# Example usage 
if __name__ == "__main__":
    # Create sample data first
    author1 = Author.objects.create(name="J.K. Rowling")
    book1 = Book.objects.create(title="Harry Potter 1", author=author1)
    book2 = Book.objects.create(title="Harry Potter 2", author=author1)
    
    library1 = Library.objects.create(name="Central Library")
    library1.books.add(book1, book2)
    
    librarian1 = Librarian.objects.create(name="Ms. Smith", library=library1)
    
    # Test queries
    get_books_by_author("J.K. Rowling")  # Using objects.filter()
    get_books_by_author_related_name("J.K. Rowling")  # Using related_name
    get_books_in_library("Central Library")
    get_librarian_for_library("Central Library")