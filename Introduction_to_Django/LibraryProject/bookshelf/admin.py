from django.contrib import admin
from .models import Book
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Fields shown in list view
    list_filter = ('author', 'publication_year')  # Filter by these fields
    search_fields = ('title', 'author')  # Enable search on these fields
