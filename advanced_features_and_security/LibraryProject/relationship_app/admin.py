from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Author, Book, Library, Librarian

# ===============================
# Custom Admin for CustomUser
# ===============================
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    Extends Django's built-in UserAdmin to include:
      - date_of_birth
      - profile_photo
      - role
    """
    model = CustomUser

    # Fields shown in the list view
    list_display = ('username', 'email', 'role', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # Fields layout when viewing/editing a user
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo', 'role')
        }),
    )

    # Fields layout when adding a new user
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo', 'role')
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


# ===============================
# Register models in admin
# ===============================
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)
