from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# ===============================
# Custom User Admin
# ===============================
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model.
    Extends Django's built-in UserAdmin to include date_of_birth, profile_photo, and role.
    """
    model = CustomUser

    list_display = ('username', 'email', 'role', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # Fields shown in edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo', 'role')
        }),
    )

    # Fields shown in add form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('date_of_birth', 'profile_photo', 'role')
        }),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)


# ===============================
# Book Admin
# ===============================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author')


# ===============================
# Register CustomUser in Admin
# ===============================
admin.site.register(CustomUser, CustomUserAdmin)
