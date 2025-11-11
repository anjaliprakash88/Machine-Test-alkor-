from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Author, Book, Borrower
from .serializers import(AuthorSerializer, 
        BookSerializer, 
        BorrowerSerializer,
        LoginSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
 

# -------------LOGIN LIST & CREATE VIEW -------------
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

# -------------AUTHOR  LIST & CREATE VIEW -------------
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

# -------------BOOK LIST & CREATE VIEW -------------
class BookListCreateView(generics.ListCreateAPIView):
    queryset           = Book.objects.select_related('author').all()
    serializer_class   = BookSerializer
    permission_classes = [IsAuthenticated]

# -------------BORROW LIST & CREATE VIEW -------------
class BorrowerListCreateView(generics.ListCreateAPIView):
    queryset           = Borrower.objects.select_related('book').all()
    serializer_class   =  BorrowerSerializer
    permission_classes = [IsAuthenticated]
