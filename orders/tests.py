from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Order
from django.contrib.auth.models import User

class OrderModelTest(TestCase):
    def test_order_status_default(self):
        user = User.objects.create_user(username='test', password='1234')
        order = Order.objects.create(user=user, book_title="کتاب تست")
        self.assertEqual(order.status, 'در انتظار بررسی')
