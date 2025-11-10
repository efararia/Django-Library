from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path("", views.book_list, name="list"),
    path("<int:book_id>/", views.book_detail, name="detail"),
    path("<int:book_id>/rating/", views.submit_rating, name="submit_rating"),
]