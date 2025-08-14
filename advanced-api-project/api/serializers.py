from .models import Author, Book
from rest_framework import serializers
from datetime import date

# Serializer for Book     
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__' # Serialize all fields in Book
    
    #Validation of publication_year not to be in the present
    def validate_publication_year(self, value):
        current_year=date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
# Serializer for Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields=('name',)
        
    #Validate that user passed a name
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Enter name")
        return value
    