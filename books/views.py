from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def book_list(request):
    q = request.GET.get("q")
    books = Book.objects.all()
    if q:
        books = books.filter(
            Q(title__icontains=q) | Q(author__icontains=q) | Q(category__icontains=q)
        )
    return render(request, "books/list.html", {"books": books, "q": q})


def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    related = Book.objects.filter(category=book.category).exclude(pk=book.pk)
    return render(request, 'books/detail.html', {'book':book, 'related':related})
