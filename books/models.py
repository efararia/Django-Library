from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=150)
    website = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    category = models.ManyToManyField(Category)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    cover = models.ImageField(upload_to="covers/", blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def get_final_price(self):
        return self.price * (1 - self.discount / 100)

class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'book') #تکرار یک بار
