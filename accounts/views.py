# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from admin_panel.models import BorrowRequest

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect("books:list")  
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

def profile(request):
    user = request.user
    date_joined = user.date_joined
    active_borrowed = BorrowRequest.objects.filter(user=user, status='approved')
    all_borrowed = BorrowRequest.objects.filter(user=user).count()
    currently_borrowed = BorrowRequest.objects.filter(user=user, status='approved').count()
    history = BorrowRequest.objects.filter(user=user).exclude(status='approved')

    return render(request, 'accounts/profile.html', {
        'active_borrowed': active_borrowed,
        'history': history,
        'all_borrowed': all_borrowed,
        'currently_borrowed': currently_borrowed,
        'date_joined': date_joined
    })