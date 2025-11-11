from django.db import models

class Author(models.Model):
    name  = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title            = models.CharField(max_length=200)
    author           = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    published_date   = models.DateField()
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Borrower(models.Model):
    name          = models.CharField(max_length=100)
    email         = models.EmailField()
    book          = models.ForeignKey(Book, related_name='borrowers', on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    return_date   = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} borrowed {self.book.title}"
