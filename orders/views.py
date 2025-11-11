from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from . forms import OrderForm
from django.contrib.auth.decorators import login_required
from books.models import Book

# Create your views here.

@login_required
def order_create(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        note = request.POST.get('note', '')
        Order.objects.create(user=request.user, book_title=book_title, note=note)
        return redirect('orders:order_list')
    return render(request, 'orders/order_create.html')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})