from django.urls import path
from .views import(AuthorListCreateView, 
BookListCreateView, 
BorrowerListCreateView,
LoginView)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('authors/', AuthorListCreateView.as_view(), name='authors'),
    path('books/', BookListCreateView.as_view(), name='books'),
    path('borrowers/', BorrowerListCreateView.as_view(), name='borrowers'),
]
