from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, BookRating
from .forms import BookRatingForm
from django.db.models import Q, Avg
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from admin_panel.models import BorrowRequest
from django.views.generic import ListView


# Create your views here.

def book_list(request):
    q = request.GET.get("q")
    books = Book.objects.all()
    if q:
        books = books.filter(
            Q(title__icontains=q)
            | Q(author__icontains=q)
            | Q(category__name__icontains=q)
        )
    
    suggested_books = None
    if request.user.is_authenticated:
        borrowed_books = BorrowRequest.objects.filter(user=request.user, status='approved').select_related('book').prefetch_related('book__category')
        
        if borrowed_books.exists():
            borrowed_categories_ids = set()
            borrowed_book_ids = set()
            
            for borrow_request in borrowed_books:
                borrowed_book_ids.add(borrow_request.book.id)
                for category in borrow_request.book.category.all():
                    borrowed_categories_ids.add(category.id)
            
            if borrowed_categories_ids:
                suggested_books = Book.objects.filter(category__id__in=borrowed_categories_ids).exclude(id__in=borrowed_book_ids).distinct()[:6]

    context = {
        "books": books,
        "q": q,
        "suggested_books": suggested_books
    }
    return render(request, "books/list.html", context)




def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    related = Book.objects.filter(category__in=book.category.all()).exclude(pk=book.pk).distinct()
    

    avg_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
    if avg_rating:
        book.rating = round(avg_rating, 1)
        book.save(update_fields=['rating'])
    else:
        book.rating = 0.0
    

    rating_count = BookRating.objects.filter(book=book).count()
    
 
    user_rating = None
    if request.user.is_authenticated:
        try:
            user_rating = BookRating.objects.get(book=book, user=request.user)
        except BookRating.DoesNotExist:
            user_rating = None
    
    context = {
        'book': book, 
        'related': related,
        'rating_count': rating_count,
        'user_rating': user_rating
    }
    
    return render(request, 'books/detail.html', context)


@login_required
def submit_rating(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    try:
        existing_rating = BookRating.objects.get(book=book, user=request.user)

    except BookRating.DoesNotExist:
        existing_rating = None
    

    if request.method == 'POST':
        if existing_rating:
            form = BookRatingForm(request.POST, instance=existing_rating)
        else:
            form = BookRatingForm(request.POST)
        
        if form.is_valid():
            rating_obj = form.save(commit=False)
            rating_obj.book = book
            rating_obj.user = request.user
            rating_obj.rating = int(form.cleaned_data['rating'])
            rating_obj.save()
            
            # به‌روزرسانی  
            avg_rating = BookRating.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg']
            if avg_rating:
                book.rating = round(avg_rating, 1)
                book.save(update_fields=['rating'])
            
            messages.success(request, 'رتبه‌بندی شما با موفقیت ثبت شد.')
            return redirect('books:detail', book_id=book_id)
    else:
        if existing_rating:
            form = BookRatingForm(instance=existing_rating)
        else:
            form = BookRatingForm()
    
    return render(request, 'books/rating_form.html', {
        'form': form,
        'book': book
    })
