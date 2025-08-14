from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
# Create your models here.
#Author model: Represents a writer who may have multiple books
class Author(models.Model):
    name=models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
    

# Book model: Represents a book linked to an author
class Book(models.Model):
    title=models.CharField(max_length=100)
    publication_year=models.IntegerField()
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books') # Reverse lookup: author.books.all()
    
    def clean(self):
        current_year=date.today().year
        if self.publication_year > current_year:
            raise ValidationError("Publication year cannot be in the future.")
        
    def save(self, *args, **kwargs):
        self.full_clean() # runs all model validations before saving
        super().save(*args, **kwargs) #writes to DB
    
    def __str__(self):
        return f"{self.title} published in {self.publication_year} by {self.author}"