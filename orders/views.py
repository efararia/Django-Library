from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from . forms import OrderForm
from django.contrib.auth.decorators import login_required
from books.models import Book

# Create your views here.

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('orders:order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/order_create.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
