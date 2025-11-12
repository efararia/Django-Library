from os import name
from django.test import TestCase
from django.test import TestCase
from django.contrib.auth.models import User
from books.models import Book, Category, Publisher, BookRating

# Create your tests here.
class BookModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="داستان", description="کتاب داستان")
        self.publisher = Publisher.objects.create(name="نشر تست")
        self.book = Book.objects.create(
            title="کتاب تست",
            author="نویسنده تست",
            year=2025,
            publisher=self.publisher,
            description="توضیحات کتاب تست",
            price=100,
            discount=20,
            stock=10,
            rating=0.0
        )
        self.book.category.add(self.category)


class BookRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.category = Category.objects.create(name="داستان", description="کتاب داستان")
        self.publisher = Publisher.objects.create(name="نشر تست")
        
        self.book = Book.objects.create(
            title="کتاب تست",
            author="نویسنده تست",
            year=2025,
            publisher=self.publisher,
            description="توضیحات کتاب تست",
            stock=5, 
            rating=0.0
        )
        self.book.category.add(self.category)

    def test_bookrating_creation(self):
        rating = BookRating.objects.create(user=self.user, book=self.book, rating=4)
        self.assertEqual(rating.rating, 4)
        self.assertEqual(rating.user.username, "testuser")
        self.assertEqual(rating.book.title, "کتاب تست")

    def test_unique_rating_per_user_and_book(self):
        BookRating.objects.create(user=self.user, book=self.book, rating=5)
        with self.assertRaises(Exception):
            BookRating.objects.create(user=self.user, book=self.book, rating=3)