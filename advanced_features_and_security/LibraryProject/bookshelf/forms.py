# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    Uses Django's ModelForm to automatically generate fields from the Book model.
    """

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # Only include relevant fields
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter publication year'}),
        }
