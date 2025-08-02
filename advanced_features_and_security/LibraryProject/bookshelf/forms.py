from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances.
    Uses Django's ModelForm to automatically generate fields from the Book model.
    """

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter author name'}),
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter publication year'}),
        }


class ExampleForm(forms.Form):
    """
    A simple example form demonstrating CSRF protection and secure input handling.
    Useful for form security demonstrations.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
        help_text="Enter your full name."
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        help_text="Enter a valid email address."
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Type your message here...'}),
        help_text="Your feedback or inquiry."
    )
