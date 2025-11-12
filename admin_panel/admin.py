from django.contrib import admin
from .models import BorrowRequest
from books.models import Book, Category, Publisher
from orders.models import Order



# Register your models here.

@admin.register(BorrowRequest)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'requested_at', 'status', 'book_rating',)
    list_editable = ('status',)
    search_fields = ('user', 'book', 'status',)
    
    def book_rating(self, obj):
        if obj.book.rating:
            return f"{round(obj.book.rating, 1)} ⭐"
        return "بدون رتبه"
    book_rating.short_description = 'RATING'


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'stock', 'display_categories', 'publisher', 'book_rating')
    search_fields = ('title', 'author')
    list_filter = ('category', 'publisher')
    filter_horizontal = ('category',)

    def book_rating(self, obj):
        if obj.rating:
            return f"{round(obj.rating, 1)} ⭐"
        return "بدون رتبه"
    book_rating.short_description = 'رتبه‌بندی'

    def display_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    display_categories.short_description = 'Categories'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class bookinline(admin.TabularInline):
    model = Book
    extra = 0
    fields = ('title', 'author', 'year',)
    readonly_fields = ('title', 'author', 'year',)

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'website',)
    search_fields = ('name',)
    inlines = [bookinline]

    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Books Count'


#Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book_title', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('book_title', 'user__username')
    readonly_fields = ('created_at',)

