from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# ===============================
# Author Model
# ===============================
class Author(models.Model):
    """
    Represents a book author.
    Fields:
        - name: The author's name (string).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        # Used in admin and shell to represent the object
        return self.name


# ===============================
# Book Model
# ===============================
class Book(models.Model):
    """
    Represents a book in the system.
    Fields:
        - title: Book's title (string).
        - author: ForeignKey linking each book to its Author.
                  on_delete=models.CASCADE means deleting an Author
                  will also delete all their books.
        - related_name='authors' allows reverse lookup from Author to Book.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    
    class Meta:
        # Custom permissions for the Book model
        permissions = [
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can change a book"),
            ("can_delete_book", "Can delete a book"),
        ]

    def __str__(self):
        return self.title


# ===============================
# Library Model
# ===============================
class Library(models.Model):
    """
    Represents a library that can hold multiple books.
    Fields:
        - name: Library name.
        - books: ManyToMany relationship to Book (a library can have many books and vice versa).
    """
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.name


# ===============================
# Librarian Model
# ===============================
class Librarian(models.Model):
    """
    Represents a librarian responsible for exactly one library.
    Fields:
        - name: Librarian's name.
        - library: OneToOneField ensures each library has exactly one librarian.
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name


# ===============================
# UserProfile Model
# ===============================
class UserProfile(models.Model):
    """
    Extends Django's built-in User model with a role field.
    Fields:
        - user: One-to-one link with Django's User.
        - role: Defines the user's role in the system (Admin, Librarian, Member).
    """
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# ===============================
# Signals: Create or update UserProfile
# ===============================
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to automatically create or update a UserProfile
    whenever a User is created or updated.
    - If 'created' is True → a new UserProfile is created.
    - Otherwise → the existing UserProfile is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
