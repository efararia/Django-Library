from django.db import models
from django.contrib.auth.models import User
from books.models import Book


class Order(models.Model):
    STATUS_CHOICES = (
        ('در انتظار بررسی', 'در انتظار بررسی'),
        ('تأیید شده', 'تأیید شده'),
        ('رد شده', 'رد شده'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255, default='کتاب نامشخص')
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.book_title} - {self.user.username}"
