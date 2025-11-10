from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from books.models import Book
from .forms import BookForm, BorrowRequestForm
from .models import BorrowRequest
from django.contrib import messages


# Create your views here.

def dashboard(request):
    books_count = Book.objects.count()
    users_count = User.objects.count()
    return render(request, 'admin_panel/dashboard.html', {
        'books_count': books_count,
        'users_count': users_count
    })

def manage_books(request):
    books = Book.objects.all()
    return render(request, 'admin_panel/manage_books.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:manage_books')
    else:
        form = BookForm()
    return render(request, 'admin_panel/book_form.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:manage_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'admin_panel/book_form.html', {'form': form})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('admin_panel:manage_books')
    return render(request, 'admin_panel/book_confirm_delete.html', {'book': book})

def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})


def borrow_book(request):
    if request.method == 'POST':
        form = BorrowRequestForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            user = request.user
            
            
            if BorrowRequest.objects.filter(user=user, status= 'approved').exists():
                messages.error(request, "شما هم‌اکنون کتابی به امانت دارید.")
                return redirect('admin_panel:borrow_book')


            if hasattr(user, 'late_returns') and user.late_returns > 2:
                messages.error(request, "شما بیش از دو بار دیرکرد داشته‌اید.")
                return redirect('admin_panel:borrow_book')


            if BorrowRequest.objects.filter(book=book, status='rejected').exists():
                messages.error(request, "این کتاب هم‌اکنون به شخص دیگری اختصاص داده شده است.")
                return redirect('admin_panel:borrow_book')

            borrow_request = form.save(commit=False)
            borrow_request.user = user
            borrow_request.book = book
            borrow_request.status = 'pending'
            borrow_request.save()

            messages.success(request, "درخواست شما ثبت شد و در انتظار تایید مدیر است.")
            return redirect('admin_panel:borrow_book')
    else:
        form = BorrowRequestForm()
    
    return render(request, 'admin_panel/borrow_book.html', {'form': form})


