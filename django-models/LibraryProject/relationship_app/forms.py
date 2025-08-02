from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book objects.
    Includes fields: title, author.
    """
    class Meta:
        model = Book
        fields = ['title', 'author'] 
