from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# ===============================
# Author Model
# ===============================
class Author(models.Model):
    """
    Represents a book author.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ===============================
# Book Model
# ===============================
class Book(models.Model):
    """
    Represents a book in the system.
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='authors')
    
    class Meta:
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
    """
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name


# ===============================
# Custom User Manager
# ===============================
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, username, and password.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Creates and saves a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)


# ===============================
# Custom User Model
# ===============================
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# ================================================================
# ADJUSTMENT NOTES FOR MIGRATION TO CUSTOM USER MODEL
# ================================================================
# 1) REMOVED UserProfile MODEL:
#    - Original project extended Django's default User model with a separate UserProfile to store roles.
#    - We replaced this with a CustomUser model that stores 'role', 'date_of_birth', and 'profile_photo' directly.
#    - This removes the need for a OneToOne link between User and UserProfile.
#    - Now we can access 'role' directly via user.role instead of user.userprofile.role.

# 2) REMOVED SIGNALS FOR USERPROFILE:
#    - Previously used post_save signals to create/update UserProfile when a User was created/updated.
#    - No longer needed because all additional fields are now part of CustomUser itself.
#    - This simplifies the code and removes the need for extra model creation on user save.

# 3) REMOVED IMPORT OF DEFAULT DJANGO USER:
#    - Original code imported from django.contrib.auth.models import User.
#    - This was replaced entirely with our CustomUser to avoid conflicts.
#    - All user references should now use get_user_model() or directly reference CustomUser.

# 4) KEPT Author, Book, Library, and Librarian MODELS UNCHANGED:
#    - These models are unrelated to authentication logic and continue to function normally.
#    - No changes required as they do not directly depend on the User model.

# 5) ADDED CustomUserManager:
#    - Custom manager for creating normal users and superusers.
#    - Handles normalization of emails and ensures all required fields are set.
#    - Ensures superusers have is_staff=True and is_superuser=True.
#    - Prepares the project for adding more custom fields in the future.

# 6) ADDED CustomUser MODEL:
#    - Extends AbstractUser to keep Django's built-in authentication features (permissions, groups, etc.).
#    - Added new fields: email (unique), date_of_birth, profile_photo, and role.
#    - Linked to CustomUserManager for proper user creation handling.
#    - Role field replaces the old UserProfile.role field.

# 7) REMOVED REDUNDANT FIELDS IN MANAGER:
#    - Kept username and password handling from AbstractUser.
#    - Only customized behavior for email and role.

# 8) OVERALL BENEFITS:
#    - Fewer models → simpler database structure.
#    - Easier role checks (no more chained lookups).
#    - Cleaner integration into admin and views.
#    - Future-proof: can add more fields directly to CustomUser without extra models.
