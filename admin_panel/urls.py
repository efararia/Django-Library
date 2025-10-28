from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.manage_books, name='manage_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
    path('users/', views.manage_users, name='manage_users'),
    path('borrow/', views.borrow_book, name='borrow_book'),
]