from rest_framework import serializers
from .models import Author, Book, Borrower
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        # Generate JWT tokens manually
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
        }


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author    = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'published_date', 'available_copies']


class BorrowerSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )

    class Meta:
        model = Borrower
        fields = '__all__'

    def validate_book(self, book):
        if book.available_copies <= 0:
            raise serializers.ValidationError("No available copies for this book.")
        return book

    def create(self, validated_data):
        book = validated_data['book']
        book.available_copies -= 1
        book.save()
        return Borrower.objects.create(**validated_data)
